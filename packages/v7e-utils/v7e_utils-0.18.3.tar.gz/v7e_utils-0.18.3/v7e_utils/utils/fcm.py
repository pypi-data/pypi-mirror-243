from __future__ import annotations

import firebase_admin
from dataclasses import dataclass
from typing import Optional
from firebase_admin import credentials, messaging


@dataclass
class FirebaseConfig:
    """
    Clase de datos que representa parámetros para una conección con Firebase.

    Args:
        type (str): Tipo de servicio.
        project_id (str): Id del project.
        private_key_id (str): Credencial privada.
        private_key (str): Cretificado.
        client_email (str): Email cliente.
        client_id (str): Id cliente.
        auth_uri (str): Url Login.
        token_uri (str): Url Token.
        auth_provider_x509_cert_url (str): Url Certificado usuario.
        client_x509_cert_url (str): Url Certificado.
        universe_domain (str): Dominio.
    """
    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str


@dataclass
class MessageTopic:
    """
    Clase de datos que representa parámetros para un mensaje push.

    Args:
        title (str): Titulo del mensaje.
        body (str): Cuerpo del mensaje.
        topic (str): Destinatarios, tema (topic) del mensaje.
        data (Optional[dict]): Diccionario opcional de parámetros a enviar.
    """
    title: str
    body: str
    topic: str
    data: Optional[dict] = None


class Fcm:
    """
    Representa una conección con Firebase Cloud Messaging.

    Args:
        config_firebase (FirebaseConfig): Parámetros de configuración para Firebase o path del json de configuración.

    Methods:
        create_message(): Genera un mensaje push.\n
        message_send(): Envia un mensaje push.\n
    """

    _message: MessageTopic | None = None

    def __init__(self, config_firebase: FirebaseConfig | str) -> None:
        """
        Inicializa una instancia de la clase Fcm.

        Args:
            config_firebase (FirebaseConfig): Parámetros de configuración de Firebase o path del json de configuración.
        """
        self.config_firebase = config_firebase
        cred = credentials.Certificate(cert=config_firebase)
        firebase_admin.initialize_app(credential=cred)
        self._message = None

    @property
    def message(self):
        """
        Almacena el valor del mesaje.
        """
        return self._message

    @message.setter
    def message(self, value: MessageTopic | None):
        """
        Cambia el valor del un mesaje.

        Args:
            value (MessageTopic | None): Mensaje de cualquier tipo valido.
        """
        self._message = value

    def create_message_topic(self, message: MessageTopic) -> Fcm:
        """
        Inicializa una instancia de la clase MessageTopic.

        Args:
            message (MessageTopic): Mensaje de tipo topic.

        Returns:
            Fcm: devuelve el self instancia.
        """
        message = messaging.Message(
            notification=messaging.Notification(
                title=message.title,
                body=message.body
            ),
            data=message.data,
            topic=message.topic
        )
        self.message = message
        return self

    def message_send(self) -> bool:
        """
        Envia una noticacion push si hay un mensaje.
        Elimina el Mensaje despues de enviado.

        Returns:
            bool: True si se envio exitosamente, False si no.
        """
        if self.message:
            response = messaging.send(self.message)
            if isinstance(response, str):
                self.message = None
                return True
        return False
