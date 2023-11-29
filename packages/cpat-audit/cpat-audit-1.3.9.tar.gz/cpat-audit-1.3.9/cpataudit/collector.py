import logging, os , pytz, json
from rq import Queue
from typing import Union
from cpataudit.auditoria import Auditoria
# https://flask.palletsprojects.com/en/2.3.x/appcontext/
from flask import request, g
from datetime import datetime
import redis
import re
from functools import wraps

logger = logging.getLogger(__name__)

TIME_ZONE = os.getenv('TIME_ZONE','Chile/Continental')
TIME_FORMAT = os.getenv('TIME_FORMAT',"%Y-%m-%dT%H:%M:%S+03:00")
santiagoTz = pytz.timezone(TIME_ZONE)

HOST_HEADER_NAME = os.getenv('HOST_HEADER_NAME', 'host')


class CollectorException(Exception):
    pass

def register_record(queue,record):
    auditoria = Auditoria()
    try:
        task = queue.enqueue(
            auditoria.save_audit_register,
            record, 
            job_timeout=os.getenv('JOB_TIME_OUT',1800), 
            result_ttl=os.environ.get('JOB_TTL_TIME', 5000)
        )
        logger.debug(task.id)
    except Exception as e:
        logger.exception(e)
        logger.warning('El registro no se ha procesado.')
        logger.warning(record)


class AuditContext(object):

    def __init__(self, queue_name, redis_host = 'redis',redis_port=6379):
        self.queue_name = queue_name
        host = os.getenv('REDIS_HOST', redis_host)
        port = os.getenv('REDIS_PORT',redis_port)
        logger.info(f'Conectando a redis {host}:{port}')
        conn = redis.Redis(host=host, port=port)

        # Cola de tareas (tasks)
        self._queue = Queue(queue_name,connection=conn)

    
    ACTION_MAP = {
        "POST": "crear",
        "GET": "leer",
        "PATCH": "modificar",
        "DELETE": "borrar",
        "PUT" : "actualizar",
    }

    def _create_record(self, request, seccion, request_method, data_detalle = None):
        detalle_data_record = None
        id_record = 1   # Default para servicios que no utilizan registros
        periodo_id_calculated = None
        try:
            detalle_data_record = request.data.decode('utf-8')
            if data_detalle:
                periodo_id_calculated = data_detalle.get('current_cpat_period')
                periodo_id_calculated = int(periodo_id_calculated) if periodo_id_calculated else None
                id_record = data_detalle.get('id_record')
            detalle_dict_record = json.loads(detalle_data_record)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            detalle_dict_record = {}
            logger.info('No se pudo decodificar el json. Tomando default "{}"')
            logger.exception(e)
        except Exception as e:
            detalle_dict_record = {}
            logger.info('No se pudo decodificar el json. Tomando default "{}"')
            logger.exception(e)

        detalle_record_json_str = json.dumps(detalle_dict_record, ensure_ascii=False)

        record = {
            "usuario_id": request.headers.get('rut'),
            "institucion_id" : request.headers.get('oae'),
            "seccion" : seccion + '/' + self.ACTION_MAP[request_method],
            "accion" : self.ACTION_MAP[request_method],
            "status" : "ok",
            "periodo_id": periodo_id_calculated,
            "registro_afectado": id_record,
            "detalle": detalle_record_json_str,
            "direccion_ip": request.headers[HOST_HEADER_NAME],
            "fecha_creacion": datetime.now(santiagoTz).strftime(TIME_FORMAT)
        } 
        return record


    def web_audit(self, seccion, method_to_filter: list = [], check_http_codes_per_path: Union[dict, None] = None):
        '''
        Funcion que colecta los datos del request que llega al endpoint.

        :param seccion: Identifica la seccion en la cual se implementa.
        :param method_to_filter: Lista de métodos que no se ejecutan. Por defecto es una lista vacía.
        :param check_http_codes_per_path (opcional): 
            Diccionario con el path y los códigos HTTP que deben retornar para ejecutar la auditoría.
            Sirve para ejecutar el path antes de la view function. Así poder acceder a los datos globales
            de Flask
            Por defecto, es None.
            Ejemplo:
                {'path': 'some/path', 'http_codes': ['200']}

        :return: Función decorada con la colección de datos.
        '''

        def decorator(func):
            logger.debug(f'Func decorator: {func}')
            @wraps(func)
            def wrapper(*args,**kwargs):

                # Check if request method is in method_to_filter
                flag_http_method_exclude = False
                request_method = request.method
                logger.warning(f'Se recibió método {request_method}')
                if request_method in method_to_filter:
                    flag_http_method_exclude = True

                logger.debug(f'Headers: {request.headers}')
                logger.debug(request.data)
    
                # Check flag_method
                if not flag_http_method_exclude:

                    if check_http_codes_per_path:
                        logger.info(f'Se recibió el path: {check_http_codes_per_path.get("path")}.')
                        logger.info(f'Se recibieron los códigos HTTP: {check_http_codes_per_path.get("http_codes")}')
                        logger.info(f'Se recibió el request path: {request.path}')
                        # Caso que se ejecutan los códigos HTTP antes de la view function.
                        if re.match(fr"{check_http_codes_per_path.get('path')}", request.path):
                            logger.info(f'Se ejecutarán los códigos HTTP antes de la view function.')
                            # Call the view function and store the response
                            response = func(*args, **kwargs)

                            # Check if the view function was successfully executed
                            if response.status_code in check_http_codes_per_path.get('http_codes'):
                                # Access the data of /some_endpoint through Flask's g object
                                # Get all keys from the g object 'data' key and store them in data_detalle
                                data_detalle = {}
                                data_detalle = g.data
                                logger.info(f'Data detalle: {data_detalle}')  # outputs: {"key1": "value1", "key2": "value2"}

                                # Pass the data to self._create_record()
                                record = self._create_record(
                                    request,
                                    seccion=seccion,
                                    request_method=request_method,
                                    data_detalle=data_detalle
                                )
                                logger.info(f'Registro creado: {record}')

                    else:
                        record = self._create_record(request, seccion=seccion, request_method=request_method)
                        logger.info(f'Registro creado else: {record}')

                error = False
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    error = True
                    logger.exception('La ejecución de la operación a encontrado un error')
                    logger.exception(e)
                    raise
                finally:
                    #No se registra nada acá, por que ya se ha registrado en el bloque except
                    if error:
                        record['estatus'] = 'error'
                    if not flag_http_method_exclude:
                        logger.info('Adding to queue')
                        register_record(self._queue, record)
            
            return wrapper
        return decorator 
