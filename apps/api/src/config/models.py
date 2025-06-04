from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel
from src.app.country.infrastructure.model.country_model import CountryModel
from src.app.continent.infrastructure.model.continent_model import ContinentModel
from src.app.vaccine.infrastructure.model.vaccine_model import VaccineModel
from src.app.user.infrastructure.model.user_model import UserModel
from src.app.role.infrastructure.model.role_model import RoleModel
from src.app.epidemic.infrastructure.model.epidemic_model import EpidemicModel
from src.app.daily_wise.infrastructure.model.daily_wise_model import DailyWiseModel
from src.app.statistic.infrastructure.model.statistic_model import StatisticModel

MODEL_REGISTRY = {
    "Country": CountryModel,
    "Continent": ContinentModel,
    "Statistic": StatisticModel,
    "Epidemic": EpidemicModel,
    "DailyWise": DailyWiseModel,
    "Vaccine": VaccineModel,
    "User": UserModel,
    "Role": RoleModel,
}
