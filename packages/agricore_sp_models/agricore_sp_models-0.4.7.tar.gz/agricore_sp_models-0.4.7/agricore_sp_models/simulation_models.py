from pydantic import BaseModel
from typing import Optional, Any, List
from enum import IntEnum

class SimulationScenario(BaseModel):
    id: Optional[int] = None
    populationId: int
    yearId: int
    shortTermModelBranch: str
    longTermModelBranch: str
    horizon: int

class LogLevel(IntEnum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class LogMessage(BaseModel):
    simulationRunId: int
    timestamp: int
    source: str
    logLevel: LogLevel
    title: str
    description: str

class OverallStatus(IntEnum):
    INPROGRESS = 1
    CANCELLED = 2
    COMPLETED = 3
    ERROR = 4

class SimulationStage(IntEnum):
    DATAPREPARATION = 1
    LONGPERIOD = 2
    LANDMARKET = 3
    SHORTPERIOD = 4
    REALISATION = 5
class SimulationRun(BaseModel):
    id: Optional[int] = None
    simulationScenarioId: int
    logMessages: Optional[List[LogMessage]] = None
    overallStatus: OverallStatus
    currentStage: SimulationStage
    currentYear: int
    currentSubStage: str
    currentStageProgress: int
    currentSubStageProgress: int
