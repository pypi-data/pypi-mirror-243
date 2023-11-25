from typing import overload
from typing import Set
from .Core import Core
from .ServiceTrigger import ServiceTrigger
from .ServiceManager_ServiceStatus import ServiceManager_ServiceStatus
from .EventService import EventService


class ServiceManager:
	"""
	Since: 1.6.3 
	"""

	@overload
	def __init__(self, runner: Core) -> None:
		pass

	@overload
	def registerService(self, name: str, pathToFile: str) -> bool:
		"""

		Args:
			name: 
			pathToFile: relative to macro folder 

		Returns:
			false if service with that name is already registered 
		"""
		pass

	@overload
	def registerService(self, name: str, pathToFile: str, enabled: bool) -> bool:
		"""

		Args:
			name: 
			pathToFile: relative to macro folder 
			enabled: 

		Returns:
			false if service with that name is already registered 
		"""
		pass

	@overload
	def registerService(self, name: str, trigger: ServiceTrigger) -> bool:
		"""

		Args:
			name: 
			trigger: 

		Returns:
			false if service with that name already registered 
		"""
		pass

	@overload
	def unregisterService(self, name: str) -> bool:
		"""

		Args:
			name: 
		"""
		pass

	@overload
	def disableReload(self, serviceName: str) -> None:
		"""
		Since: 1.8.4 

		Args:
			serviceName: the name of the service to disable the reload feature for 
		"""
		pass

	@overload
	def renameService(self, oldName: str, newName: str) -> bool:
		"""

		Args:
			newName: 
			oldName: 

		Returns:
			false if service with new name already registered or old name doesn't exist 
		"""
		pass

	@overload
	def getServices(self) -> Set[str]:
		"""

		Returns:
			registered service names 
		"""
		pass

	@overload
	def startService(self, name: str) -> ServiceManager_ServiceStatus:
		"""starts service once

		Args:
			name: service name 

		Returns:
			previous state (or ServiceManager_ServiceStatus#UNKNOWN if unknown service) 
		"""
		pass

	@overload
	def stopService(self, name: str) -> ServiceManager_ServiceStatus:
		"""

		Args:
			name: service name 

		Returns:
			previous state (or ServiceManager_ServiceStatus#UNKNOWN if unknown service) 
		"""
		pass

	@overload
	def restartService(self, name: str) -> ServiceManager_ServiceStatus:
		"""

		Args:
			name: service name 

		Returns:
			state before "restarting" (or ServiceManager_ServiceStatus#UNKNOWN if unknown service) 
		"""
		pass

	@overload
	def enableService(self, name: str) -> ServiceManager_ServiceStatus:
		"""

		Args:
			name: service name 

		Returns:
			previous state (or ServiceManager_ServiceStatus#UNKNOWN if unknown service) 
		"""
		pass

	@overload
	def disableService(self, name: str) -> ServiceManager_ServiceStatus:
		"""

		Args:
			name: service name 

		Returns:
			previous state (or ServiceManager_ServiceStatus#UNKNOWN if unknown service) 
		"""
		pass

	@overload
	def isRunning(self, name: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			name: the name of the service to check 

		Returns:
			'true' if the service is running, 'false' otherwise. 
		"""
		pass

	@overload
	def isEnabled(self, name: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			name: the name of the service to check 

		Returns:
			'true' if the service is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def status(self, name: str) -> ServiceManager_ServiceStatus:
		"""

		Args:
			name: service name 

		Returns:
			ServiceManager_ServiceStatus#UNKNOWN if unknown service, ServiceManager_ServiceStatus#RUNNING if disabled and running, ServiceManager_ServiceStatus#DISABLED if disabled and stopped, ServiceManager_ServiceStatus#STOPPED if enabled and stopped, ServiceManager_ServiceStatus#ENABLED if enabled and running. 
		"""
		pass

	@overload
	def getServiceData(self, name: str) -> EventService:
		"""this might throw if the service is not running...\n
		Since: 1.6.5 

		Args:
			name: 

		Returns:
			the event that is current for the service 
		"""
		pass

	@overload
	def getTrigger(self, name: str) -> ServiceTrigger:
		"""
		Since: 1.6.5 [named getServiceData previously] 

		Args:
			name: 
		"""
		pass

	@overload
	def load(self) -> None:
		"""load services from config
		"""
		pass

	@overload
	def save(self) -> None:
		"""save current registered services enabled/disabled status to config
		"""
		pass

	@overload
	def stopReloadListener(self) -> None:
		"""Stops the service manager from reloading scrips on file changes.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def startReloadListener(self) -> None:
		"""Will make the service manager reload scripts on file changes.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def markCrashed(self, serviceName: str) -> None:
		"""Mark a service as crashed so that it can be reloaded when its file changes. Crashed services
must be marked so that file change listener knows to restart them even if they are not
running because they crashed.\n
		Since: 1.8.4 

		Args:
			serviceName: the name of the service to mark as crashed 
		"""
		pass

	@overload
	def isCrashed(self, serviceName: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			serviceName: the name of the service to check 

		Returns:
			'true' if the service previously crashed, 'false' otherwise. 
		"""
		pass

	@overload
	def tickReloadListener(self) -> None:
		"""Ticks the service manager. This will check if any services need to be reloaded and reloads
them if necessary.\n
		Since: 1.8.4 
		"""
		pass

	pass


