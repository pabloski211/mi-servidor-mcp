
from mock_confluence_service import pages
import os
from mcp.server.fastmcp import FastMCP
from fastapi.middleware.cors import CORSMiddleware


PORT=os.environ.get("PORT", 8000)
mcp = FastMCP("MCP DOCUMENTAL",host="0.0.0.0", port=PORT)

import os

# --- Configuración del Servidor ---
PORT = os.environ.get("PORT", 8000)

# 1. Configuración del título, versión y descripción directamente en FastMCP
mcp = FastMCP(
    "HR MCP Server",  # Este será el nombre/título
    host="0.0.0.0",
    port=PORT
)

# 2. Añadir Middleware CORS a la aplicación FastAPI subyacente
# FastMCP expone la aplicación de FastAPI a través del atributo `.app`
mcp.app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Asumimos que 'mcp' es un módulo o objeto disponible en tu entorno,
# similar al ejemplo que proporcionaste.
# import mcp 

@mcp.tool()
def search_documents() -> str:
    """
    Use this tool to search for VMware documentation.
    This is a mock function that simulates searching a knowledge base for VMware-related documents.
    It returns a formatted string with information about products like vSphere, ESXi, and NSX.

    Returns:
        str: A formatted string containing mock information about VMware documentation.
    """
    # Este es un string simulado (mock) que podría venir de una base de datos o una API.
    mock_vmware_docs = """
Resultados de la búsqueda de documentación de VMware:

--------------------------------------------------
Título: Guía de Administración de vSphere 8
Resumen: Cubre la instalación, configuración y gestión de vCenter Server y hosts ESXi. Incluye temas sobre redes, almacenamiento y máquinas virtuales.
Ubicación: /docs/vsphere/8/admin-guide.pdf
--------------------------------------------------
Título: Referencia de la API de vCenter
Resumen: Documentación completa para desarrolladores sobre cómo interactuar programáticamente con vCenter Server usando la API de REST.
Ubicación: /docs/vsphere/8/api-reference.html
--------------------------------------------------
Título: Guía de Seguridad de VMware NSX
Resumen: Mejores prácticas y configuraciones para asegurar tu entorno de red virtualizado con NSX Data Center. Cubre microsegmentación, firewalls y VPN.
Ubicación: /docs/nsx/security-guide.md
--------------------------------------------------
Título: Cómo solucionar problemas de rendimiento en ESXi
Resumen: Artículo de la base de conocimientos que describe herramientas y técnicas comunes para diagnosticar y resolver problemas de rendimiento en hosts ESXi.
Ubicación: /kb/esxi/performance-troubleshooting
--------------------------------------------------
Título: Introducción a VMware Cloud on AWS
Resumen: Descripción general del servicio que ejecuta la infraestructura de VMware SDDC en la nube de Amazon Web Services.
Ubicación: /docs/vmc-on-aws/introduction.pdf
--------------------------------------------------
"""
    # Usamos .strip() para limpiar los saltos de línea al principio y al final del string.
    return mock_vmware_docs.strip()

# Asumimos que 'mcp' es un módulo o objeto disponible en tu entorno.
# import mcp

@mcp.tool()
def get_incident_resolution_examples() -> str:
    """
    Use this tool to get examples of resolved IT incidents.
    This is a mock function that simulates querying a ticketing system or knowledge base
    for past incidents and their solutions. It's useful for finding how similar problems were solved.

    Returns:
        str: A formatted string containing mock examples of resolved incidents.
    """
    # String simulado con ejemplos de incidencias resueltas.
    mock_incidents = """
Ejemplos de Resolución de Incidencias:

--------------------------------------------------
ID de Incidencia: INC-001234
Título: Usuario no puede iniciar sesión en la aplicación CRM
Síntomas: El usuario recibe un error de "Credenciales inválidas" tras varios intentos. Otros usuarios no reportan problemas.
Causa Raíz: La cuenta del usuario había sido bloqueada por la política de seguridad tras múltiples intentos fallidos.
Resolución: Se verificó la identidad del usuario a través de una videollamada y se desbloqueó su cuenta. Se le recomendó usar el flujo de "olvidé mi contraseña".
Estado: Resuelto
--------------------------------------------------
ID de Incidencia: INC-001235
Título: Servicio de pagos en línea no responde
Síntomas: Los clientes reportan errores de timeout al intentar realizar un pago. El monitor de salud del servicio muestra "CRÍTICO".
Causa Raíz: Una actualización reciente del servicio introdujo un bug de memoria que causaba que el proceso se detuviera inesperadamente.
Resolución: Se realizó un rollback a la versión estable anterior del servicio. Se reiniciaron los servicios afectados. El equipo de desarrollo fue notificado para corregir el bug.
Estado: Resuelto (Mitigado)
--------------------------------------------------
ID de Incidencia: INC-001236
Título: Rendimiento lento en la base de datos de reportes
Síntomas: La generación de reportes que normalmente tarda 2 minutos, ahora toma más de 15 minutos.
Causa Raíz: Una consulta SQL ineficiente para un nuevo reporte estaba consumiendo un exceso de recursos de CPU y I/O.
Resolución: Se identificó y optimizó la consulta SQL problemática. Se añadieron los índices necesarios a la tabla para mejorar el rendimiento.
Estado: Resuelto
--------------------------------------------------
"""
    # Usamos .strip() para limpiar los saltos de línea al principio y al final del string.
    return mock_incidents.strip()
