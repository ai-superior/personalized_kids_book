import abc

from domain.leads.model import Lead


class LeadRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, lead: Lead):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, lead_id: str) -> Lead:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[Lead]:
        raise NotImplementedError
