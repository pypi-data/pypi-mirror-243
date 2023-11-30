from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction
from rest_framework import serializers


class DefaultSerializer(serializers.ModelSerializer):
    """
    Clase para serializer personalizado permitiendo filtrar los campos serializados según una lista proporcionada en el contexto.

    Methods:
        to_representation(): Converte una instancia de modelo en una representación serializada.
.
    """
    def __init__(self, *args, **kwargs):
        # Obtener y eliminar el parámetro 'exclude_field' si está presente
        self.exclude_field = kwargs.pop('exclude_field', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        """
        Converte una instancia de modelo en una representación serializada.

        Args:
            instance : Instancia del modelo.

        Returns:
            serializers: Representación serializada de la instancia del modelo.
        """
        context = self.context
        fields_list = context.get('fields', [])

        if fields_list:
            data = super().to_representation(instance)
            filtered_data = {key: value for key, value in data.items() if key in fields_list}
        else:
            filtered_data = super().to_representation(instance)

        if self.exclude_field and self.exclude_field in filtered_data:
            del filtered_data[self.exclude_field]

        return filtered_data


class DefaultResponse(Response):
    """
    Clase que hereda de Response para respuesta personalizada que incluye información adicional como mensaje, datos, estado, notificación, etc.

    Args:
        message
        data
        status 
        error_code
        notification
        notification_type
        template_name 
        headers 
        exception (bool)
        content_type
    """
    def __init__(self, message=None, data=None, status=None, error_code=None, notification=None,
                 notification_type=None, template_name=None, headers=None, exception=False, content_type=None):

        if message is None:
            raise ValidationError(detail={'message': ['Message is required']})
        if status is None:
            raise ValidationError(detail={'message': ['Status is required']})
        if notification is not None:
            if notification_type is None:
                raise ValidationError(detail={'message': ['notification_type is required']})

        if exception and error_code:
            data['error_code'] = error_code

        response_data = {
            'message': message,
            'data': data,
            'status_code': status,
            'notification': notification,
            'notification_type': notification_type
        }
        super().__init__(data=response_data, status=status, template_name=template_name,
                         headers=headers, exception=exception, content_type=content_type)


def validate_required_fields(data, required_fields, allow_empty_fields={}):
    """
        Función para validar la presencia de campos requeridos en los datos.

        Args:
            data (dict): El conjunto de datos que se va a validar.
            required_fields (list): Lista de nombres de campos que son obligatorios.
            allow_empty_fields (dict): Diccionario opcional que especifica campos que se permiten estar vacíos.

        Returns:
            DefaultResponse or None: Devuelve una respuesta personalizada si la validación falla, o None si la validación es exitosa.
    """
    for field_name in required_fields:
        field_value = data.get(field_name)

        if field_value is None or (field_name not in allow_empty_fields and not field_value):
            return DefaultResponse(message=f"The field '{field_name}' is required",
                                   status=400)


def validate_and_clean_data(data, required_fields):
    """
        Función para validar y limpiar los datos, asegurándose de que los campos requeridos estén presentes.

        Args:
            data (dict): El conjunto de datos que se va a validar y limpiar.
            required_fields (list): Lista de nombres de campos que son obligatorios.

        Returns:
            dict or DefaultResponse: Datos limpiados si la validación es exitosa, o una respuesta personalizada si la validación falla.
        """
    cleaned_data = {}

    # Validar campos requeridos y realizar limpieza
    for field_name in required_fields:
        if field_name not in data or data[field_name] is None or data[field_name] == '':
            return DefaultResponse(message=f"The field '{field_name}' is required",
                                   status=status.HTTP_400_BAD_REQUEST)
        cleaned_data[field_name] = data[field_name]

    # Eliminar campos adicionales que no están en required_fields
    for field_name in data:
        if field_name not in required_fields:
            print(f"Warning: Field '{field_name}' is not in required_fields and will be removed.")

    return cleaned_data


class DefaultViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas personalizado que proporciona acciones predeterminadas y respuestas personalizadas.

    Methods:
        select_list(): Acción personalizada para obtener una lista seleccionada de objetos.
        create(): Acción para crear un objeto con validación y manejo de transacciones.
        update(): Acción para actualizar un objeto con validación y manejo de transacciones.
        partial_update(): Acción para actualizar parcialmente un objeto con validación y manejo de transacciones.
        destroy(): Acción para eliminar un objeto con manejo de transacciones.
    """
    @action(detail=False, methods=['GET'], url_name='select_list')
    def select_list(self, request):
        """
        Acción personalizada para obtener una lista seleccionada de objetos.
        """
        try:
            fields_param = request.query_params.get('fields', None)
            order_by = request.query_params.get('order_by', None)
            fields_list = []
            allowed_fields = [field.name for field in self.get_queryset().model._meta.fields]
            search_query = request.query_params.get('search', None)

            if fields_param:
                fields_list = fields_param.split(',')
                fields_list = [field for field in fields_list if field in allowed_fields]
                queryset = self.get_queryset().values(*fields_list)
            else:
                queryset = self.get_queryset()

            if search_query:
                queryset = self.filter_queryset(queryset)

            if order_by:
                if order_by.lstrip('-') in allowed_fields:
                    queryset = queryset.order_by(order_by)

            serializer = self.get_serializer(queryset, many=True, context={'fields': fields_list})
            return DefaultResponse(message='Objects successfully gotten', data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return DefaultResponse(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """
        Acción para crear un objeto con validación y manejo de transacciones.
        """
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return DefaultResponse(message='Object successfully created',
                                   data=serializer.data,
                                   status=status.HTTP_201_CREATED)
        except Exception as e:
            errors = e.detail
            error_messages = "\n".join(
                [f"Field: {field}, Error: {', '.join(messages)}"
                 for field, messages in errors.items()]
            )
            return DefaultResponse(message=error_messages,
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Acción para actualizar un objeto con validación y manejo de transacciones.
        """
        try:
            with transaction.atomic():
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
            return DefaultResponse(message='Object successfully updated',
                                   data=serializer.data,
                                   status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return DefaultResponse(message=error_message,
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        """
        Acción para actualizar parcialmente un objeto con validación y manejo de transacciones.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Acción para eliminar un objeto con manejo de transacciones.
        """
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.delete()
            return DefaultResponse(message='Object successfully deleted',
                                   status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            error_message = str(e)
            return DefaultResponse(message=error_message,
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)
