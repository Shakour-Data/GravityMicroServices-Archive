"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : services.py
Description  : Service discovery API endpoints.
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : None
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-07 21:30 UTC
Last Modified     : 2025-11-07 21:30 UTC
Development Time  : 1 hour 30 minutes
Review Time       : 0 hours 20 minutes
Testing Time      : 0 hours 40 minutes
Total Time        : 2 hours 30 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 1.5 × $150 = $225.00 USD
Review Cost       : 0.33 × $150 = $50.00 USD
Testing Cost      : 0.67 × $150 = $100.00 USD
Total Cost        : $375.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-07 - Elena Volkov - Initial implementation

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : app.services, app.schemas, app.core
External  : fastapi, sqlalchemy
Database  : PostgreSQL 16+

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

================================================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging
import asyncio
import json

from app.core.database import get_db
from app.services.registry_service import ServiceRegistryService
from app.schemas.service import (
    ServiceRegister,
    ServiceResponse,
    ServiceDiscoveryRequest,
    ServiceInstanceResponse,
    ServiceListResponse,
    ServiceDeregister,
    HealthCheckUpdate,
    ServiceEventResponse,
    AllServicesResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/services/register",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a service",
    description="Register a new service instance with the discovery service"
)
async def register_service(
    service_data: ServiceRegister,
    db: AsyncSession = Depends(get_db)
) -> ServiceResponse:
    """
    Register a new service instance.
    
    Args:
        service_data: Service registration data
        db: Database session
        
    Returns:
        Registered service information
    """
    logger.info(f"API: Register service request for {service_data.service_id}")
    
    try:
        registry = ServiceRegistryService(db)
        service = await registry.register_service(service_data)
        
        return ServiceResponse.model_validate(service)
        
    except Exception as e:
        logger.exception(f"Error registering service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register service: {str(e)}"
        )


@router.post(
    "/services/deregister",
    status_code=status.HTTP_200_OK,
    summary="Deregister a service",
    description="Remove a service instance from the registry"
)
async def deregister_service(
    deregister_data: ServiceDeregister,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Deregister a service instance.
    
    Args:
        deregister_data: Service deregistration data
        db: Database session
        
    Returns:
        Success message
    """
    logger.info(f"API: Deregister service request for {deregister_data.service_id}")
    
    try:
        registry = ServiceRegistryService(db)
        success = await registry.deregister_service(deregister_data.service_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service not found: {deregister_data.service_id}"
            )
        
        return {
            "success": True,
            "message": f"Service {deregister_data.service_id} deregistered successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error deregistering service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deregister service: {str(e)}"
        )


@router.post(
    "/services/discover",
    response_model=ServiceInstanceResponse,
    summary="Discover service instance",
    description="Discover and select a service instance using load balancing"
)
async def discover_service(
    discovery_request: ServiceDiscoveryRequest,
    db: AsyncSession = Depends(get_db)
) -> ServiceInstanceResponse:
    """
    Discover a service instance.
    
    Applies load balancing strategy to select an instance.
    
    Args:
        discovery_request: Service discovery parameters
        db: Database session
        
    Returns:
        Selected service instance
    """
    logger.info(f"API: Discover service request for {discovery_request.service_name}")
    
    try:
        registry = ServiceRegistryService(db)
        instance = await registry.discover_service(discovery_request)
        
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No instances found for service: {discovery_request.service_name}"
            )
        
        return ServiceInstanceResponse(
            service_id=instance.service_id,
            service_name=instance.service_name,
            address=instance.address,
            port=instance.port,
            tags=instance.tags,
            meta=instance.meta,
            health_status=instance.health_status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error discovering service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to discover service: {str(e)}"
        )


@router.post(
    "/services/discover/all",
    response_model=AllServicesResponse,
    summary="Discover all service instances",
    description="Retrieve all instances of a service"
)
async def discover_all_instances(
    discovery_request: ServiceDiscoveryRequest,
    db: AsyncSession = Depends(get_db)
) -> ServiceListResponse:
    """
    Get all instances of a service.
    
    Args:
        discovery_request: Service discovery parameters
        db: Database session
        
    Returns:
        List of all service instances
    """
    logger.info(f"API: Discover all instances for {discovery_request.service_name}")
    
    try:
        registry = ServiceRegistryService(db)
        instances = await registry.get_all_instances(discovery_request)
        
        service_instances = [
            ServiceInstanceResponse(
                service_id=inst.service_id,
                service_name=inst.service_name,
                address=inst.address,
                port=inst.port,
                tags=inst.tags,
                meta=inst.meta,
                health_status=inst.health_status
            )
            for inst in instances
        ]
        
        return ServiceListResponse(
            services=service_instances,
            total=len(service_instances),
            strategy_used=discovery_request.lb_strategy.value if discovery_request.lb_strategy is not None else ""
        )
        
    except Exception as e:
        logger.exception(f"Error discovering all instances: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to discover instances: {str(e)}"
        )


@router.get(
    "/services",
    response_model=AllServicesResponse,
    summary="Get all services",
    description="Get summary of all registered services"
)
async def get_all_services(
    db: AsyncSession = Depends(get_db)
) -> AllServicesResponse:
    """
    Get all registered services.
    
    Args:
        db: Database session
        
    Returns:
        Summary of all services
    """
    logger.info("API: Get all services request")
    
    try:
        registry = ServiceRegistryService(db)
        services = await registry.get_all_services()
        
        total_instances = sum(len(tags) for tags in services.values())
        
        return AllServicesResponse(
            services=services,
            total_services=len(services),
            total_instances=total_instances
        )
        
    except Exception as e:
        logger.exception(f"Error getting all services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get services: {str(e)}"
        )


@router.post(
    "/health/update",
    summary="Update health check",
    description="Update TTL-based health check status"
)
async def update_health_check(
    health_update: HealthCheckUpdate,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Update TTL health check.
    
    Args:
        health_update: Health check update data
        db: Database session
        
    Returns:
        Success message
    """
    logger.info(f"API: Update health check for {health_update.check_id}")
    
    try:
        registry = ServiceRegistryService(db)
        success = await registry.update_health_check(
            health_update.check_id,
            health_update.status,
            health_update.output if health_update.output is not None else ""
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update health check"
            )
        
        return {
            "success": True,
            "message": f"Health check updated: {health_update.check_id}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error updating health check: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update health check: {str(e)}"
        )


@router.get(
    "/events/{service_id}",
    response_model=List[ServiceEventResponse],
    summary="Get service events",
    description="Get event history for a specific service"
)
async def get_service_events(
    service_id: str,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> List[ServiceEventResponse]:
    """
    Get service events.
    
    Args:
        service_id: Service instance ID
        limit: Maximum number of events
        db: Database session
        
    Returns:
        List of service events
    """
    logger.info(f"API: Get events for service {service_id}")
    
    try:
        registry = ServiceRegistryService(db)
        events = await registry.get_service_events(service_id, limit)
        
        return [ServiceEventResponse.model_validate(event) for event in events]
        
    except Exception as e:
        logger.exception(f"Error getting service events: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get events: {str(e)}"
        )


@router.get(
    "/events",
    response_model=List[ServiceEventResponse],
    summary="Get all events",
    description="Get recent events for all services"
)
async def get_all_events(
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> List[ServiceEventResponse]:
    """
    Get all service events.
    
    Args:
        limit: Maximum number of events
        db: Database session
        
    Returns:
        List of service events
    """
    logger.info("API: Get all events")
    
    try:
        registry = ServiceRegistryService(db)
        events = await registry.get_service_events(None, limit)
        
        return [ServiceEventResponse.model_validate(event) for event in events]
        
    except Exception as e:
        logger.exception(f"Error getting all events: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get events: {str(e)}"
        )


@router.delete(
    "/services/deregister/{service_id}",
    status_code=status.HTTP_200_OK,
    summary="Deregister service by ID",
    description="Remove a service instance using path parameter"
)
async def deregister_service_by_id(
    service_id: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Deregister a service instance using path parameter.
    
    Args:
        service_id: Service instance ID
        db: Database session
        
    Returns:
        Success message
    """
    logger.info(f"API: Deregister service {service_id} via DELETE")
    
    try:
        registry = ServiceRegistryService(db)
        success = await registry.deregister_service(service_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service not found: {service_id}"
            )
        
        return {
            "success": True,
            "message": f"Service {service_id} deregistered successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error deregistering service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deregister service: {str(e)}"
        )


@router.get(
    "/services/{service_name}/instance",
    response_model=ServiceInstanceResponse,
    summary="Get service instance with load balancing",
    description="Discover and select a service instance using query parameters"
)
async def get_service_instance(
    service_name: str,
    strategy: str = "round_robin",
    region: str | None = None,
    zone: str | None = None,
    datacenter: str | None = None,
    db: AsyncSession = Depends(get_db)
) -> ServiceInstanceResponse:
    """
    Get a service instance with load balancing.
    
    Args:
        service_name: Name of the service to discover
        strategy: Load balancing strategy (round_robin, weighted, least_connections, geographic, random)
        region: Region for geographic routing
        zone: Zone for geographic routing  
        datacenter: Datacenter for geographic routing
        db: Database session
        
    Returns:
        Selected service instance
    """
    logger.info(f"API: Get instance for {service_name} with strategy {strategy}")
    
    try:
        from app.schemas.service import LoadBalancingStrategy
        
        # Create discovery request
        discovery_request = ServiceDiscoveryRequest(
            service_name=service_name,
            lb_strategy=LoadBalancingStrategy(strategy),
            region=region,
            zone=zone,
            datacenter=datacenter
        )
        
        registry = ServiceRegistryService(db)
        instance = await registry.discover_service(discovery_request)
        
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No instances found for service: {service_name}"
            )
        
        return ServiceInstanceResponse(
            service_id=instance.service_id,
            service_name=instance.service_name,
            address=instance.address,
            port=instance.port,
            tags=instance.tags,
            meta=instance.meta,
            health_status=instance.health_status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error getting service instance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get service instance: {str(e)}"
        )


@router.get(
    "/config/{key}",
    summary="Get configuration value",
    description="Retrieve a configuration value from Consul KV store"
)
async def get_config(
    key: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get configuration value from Consul KV store.
    
    Args:
        key: Configuration key
        db: Database session
        
    Returns:
        Configuration value
    """
    logger.info(f"API: Get config for key: {key}")
    
    try:
        from app.core.consul_client import consul_client
        
        value = await consul_client.get_kv(key)
        
        if value is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuration key not found: {key}"
            )
        
        return {
            "key": key,
            "value": value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error getting config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get configuration: {str(e)}"
        )


@router.put(
    "/config/{key}",
    status_code=status.HTTP_200_OK,
    summary="Set configuration value",
    description="Store a configuration value in Consul KV store"
)
async def set_config(
    key: str,
    value: dict,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Set configuration value in Consul KV store.
    
    Args:
        key: Configuration key
        value: Configuration value (must contain 'value' field)
        db: Database session
        
    Returns:
        Success message
    """
    logger.info(f"API: Set config for key: {key}")
    
    try:
        from app.core.consul_client import consul_client
        
        config_value = value.get("value", "")
        if not isinstance(config_value, str):
            config_value = str(config_value)
        
        success = await consul_client.put_kv(key, config_value)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store configuration"
            )
        
        return {
            "success": True,
            "key": key,
            "message": "Configuration stored successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error setting config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set configuration: {str(e)}"
        )


@router.websocket("/config/watch/{key}")
async def watch_config(
    websocket: WebSocket,
    key: str
):
    """
    Watch configuration changes in real-time via WebSocket.
    
    Watches a specific configuration key in Consul KV store and sends
    updates to the client when the value changes.
    
    Args:
        websocket: WebSocket connection
        key: Configuration key to watch
        
    WebSocket Messages:
        - Send: {"key": str, "value": str, "index": int}
        - Receive: {"command": "ping"} for keepalive
    """
    await websocket.accept()
    logger.info(f"WebSocket: Client connected to watch key: {key}")
    
    try:
        from app.core.consul_client import consul_client
        
        # Send initial value
        initial_value = await consul_client.get_kv(key)
        await websocket.send_json({
            "key": key,
            "value": initial_value,
            "index": 0,
            "action": "initial"
        })
        
        last_value = initial_value
        index = 0
        
        # Poll for changes (in production, use Consul's blocking queries)
        while True:
            try:
                # Check for client messages (ping/pong)
                try:
                    message = await asyncio.wait_for(
                        websocket.receive_json(),
                        timeout=0.1
                    )
                    if message.get("command") == "ping":
                        await websocket.send_json({"command": "pong"})
                except asyncio.TimeoutError:
                    pass
                
                # Poll for value changes every 2 seconds
                await asyncio.sleep(2)
                
                current_value = await consul_client.get_kv(key)
                
                # Send update if value changed
                if current_value != last_value:
                    index += 1
                    await websocket.send_json({
                        "key": key,
                        "value": current_value,
                        "index": index,
                        "action": "update"
                    })
                    last_value = current_value
                    logger.info(f"WebSocket: Sent config update for key: {key}")
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket: Client disconnected from key: {key}")
                break
            except Exception as e:
                logger.error(f"WebSocket: Error watching key {key}: {e}")
                await websocket.send_json({
                    "error": str(e),
                    "action": "error"
                })
                break
                
    except Exception as e:
        logger.exception(f"WebSocket: Fatal error for key {key}: {e}")
        try:
            await websocket.close(code=1011, reason=str(e))
        except:
            pass
