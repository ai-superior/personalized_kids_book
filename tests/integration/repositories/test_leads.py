from dependencies import DependencyInjector

from domain.leads.model import Lead
from domain.leads.repositories import LeadRepository


def test_get_all_leads(lead: Lead):
    repo: LeadRepository = DependencyInjector.get().leads()
    leads = repo.list()
    assert len(leads) >= 1


def test_get_lead(lead: Lead):
    repo: LeadRepository = DependencyInjector.get().leads()
    lead_collection = repo.get(lead.id)
    assert lead_collection.id == lead.id
