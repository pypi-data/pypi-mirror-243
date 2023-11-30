from pydantic import BaseModel
from typing import Optional
from enum import IntEnum

class AgriculturalProduction(BaseModel):
    id: Optional[int] = None
    farmId: int
    yearId: int
    productGroupId: Optional[int] = None
    valueSales: float
    quantitySold: float
    cropProduction: float
    irrigatedArea: float
    cultivatedArea: float
    organicProductionType: int
    variableCosts: float
    landValue: float
    
class LivestockProduction(BaseModel):
    id: Optional[int] = None
    farmId: int
    yearId: int
    productGroupId: Optional[int] = None
    numberOfAnimals: float
    numberOfAnimalsSold: int
    valueSoldAnimals: float
    numberAnimalsForSlaughtering: int
    valueSlaughteredAnimals: float
    numberAnimalsRearingBreading: float
    valueAnimalsRearingBreading: float
    milkTotalProduction: float
    milkProductionSold: float
    milkTotalSales: float
    milkVariableCosts: float
    woolTotalProduction: float
    woolProductionSold: float
    eggsTotalSales: float
    eggsTotalProduction: float
    eggsProductionSold: float
    manureTotalSales: float
    dairyCows: int
    variableCosts: float

class Population(BaseModel):
    id: Optional[int] = None
    description: str
    
class Farm(BaseModel):
    id: Optional[int] = None
    populationId: Optional[int] = None
    lat: int
    long: int
    altitude: int
    regionLevel1: int
    regionLevel1Name: str
    regionLevel2: int
    regionLevel2Name: str
    regionLevel3: int
    regionLevel3Name: str
    farmCode: str
    technicalEconomicOrientation: int
    weight_ra: float
    weight_reg: float
        
class ProductGroup(BaseModel):
    id: Optional[int] = None
    populationId: Optional[int] = None
    name: str
    productType: int
    originalNameDatasource: str
    productsIncludedInOriginalDataset: str
    
class FADNProductRelation(BaseModel):
    id: Optional[int] = None
    productGroupId: Optional[int] = None
    fadnProductId: Optional[int] = None
    populationId: Optional[int] = None

class ClosingValue(BaseModel):
    id: Optional[int] = None
    agriculturalLand: float
    landImprovements: float
    forestLand: float
    farmBuildings: float
    machineryAndEquipment: float
    intangibleAssetsTradable: float
    intangibleAssetsNonTradable: float
    otherNonCurrentAssets: float
    longAndMediumTermLoans: float
    totalCurrentAssets: float
    farmNetIncome: float
    grossFarmIncome: float
    subsidiesOnInvestments: float
    vatBalanceOnInvestments: float
    totalOutputCropsAndCropProduction: float
    totalOutputLivestockAndLivestockProduction: float
    otherOutputs: float
    totalIntermediateConsumption: float
    taxes: float
    vatBalanceExcludingInvestments: float
    fixedAssets: float
    depreciation: float
    totalExternalFactors: float
    machinery: float
    farmId: int
    yearId: int
    averageHaPrice: float
    
class Policy(BaseModel):
    id: Optional[int] = None
    policyIdentifier: str
    policyDescription: str
    isCoupled: bool
    
class PolicyProductGroupRelation(BaseModel):
    id: Optional[int] = None
    productGroupId: int
    policyId: int
    populationId: Optional[int] = None

class HolderFarmYearData(BaseModel):
    id: Optional[int] = None
    farmId: Optional[int] = None
    yearId: Optional[int] = None
    holderAge: int
    holderGender: int
    holderSuccessors: int
    holderSuccessorsAge: int
    holderFamilyMembers: int

class ValueToLPDTO(BaseModel):
    farmId: int
    yearId: int
    a_0: float
    sE465: float
    sE490: float
    averageHAPrice: float
    sE420: float
    sE410: float
    aversionRiskFactor: float
    m_0: float

class ValueFromLPDTO(BaseModel):
    farmId: int
    yearId: int
    agriculturalLand: float
    totalCurrentAssests: float
    agriculturalLandHectaresAdquisition: float
    longAndMediumTermLoans: float
    averageHAPrice: float
    agriculturalLandHectares: float

class CropDataDTO(BaseModel):

    cropProductiveArea: int
    cropVariableCosts: float
    cropProduction: float
    cropSellingPrice: float
    coupledSubsidy: float
    uAA: float
class ValueFromSPDTO(BaseModel):

    farmId: int

    totalCurrentAssets: float
    farmNetIncome: float
    farmGrossIncome: float
    agriculturalLand: float
    crops: dict[str,CropDataDTO]

class LivestockDTO(BaseModel):
    numberOfAnimals: float
    dairyCows: int
    rebreedingCows: float
    milkProduction: float
    milkSellingPrice: float
    variableCosts: float

class DecoupledSubsidiesDTO(BaseModel):
    pGreen: float
    pBasic: float

class HolderInfoDTO(BaseModel):
    holderAge: int
    holderSuccessorsAge: int
    holderSuccessors: int
    holderFamilyMembers: int

class AltitudeEnum(IntEnum):
    MOUNTAINS = 1
    HILLS = 2
    PLAINS = 3

class ValueToSPDTO(BaseModel):
    farmCode: int
    holderInfo: HolderInfoDTO
    cod_RAGR: int
    cod_RAGR3: int
    technicalEconomicOrientation: int
    altitude: AltitudeEnum
    currentAssets: float
    decoupledSubsidies: DecoupledSubsidiesDTO
    crops: dict[str,CropDataDTO]
    livestock: LivestockDTO

class IntermediateValueFromLP(BaseModel):
    farmId: int
    averageHAPrice: float
    previousAgriculturalLand: float
    result: dict
