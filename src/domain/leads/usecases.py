import abc

from domain.basic_types import UseCase
from domain.leads import queries, errors, commands, model
from domain.leads.model import Lead
from domain.leads.repositories import LeadRepository
from domain.leads.services import LLMProcessor


class StandardRequestUseCase(UseCase, abc.ABC):
    def __init__(self, messages: LeadRepository):
        super().__init__()
        self.messages = messages


class GetMessage(StandardRequestUseCase):
    def execute(self, query: queries.GetLead) -> Lead:
        lead = self.messages.get(query.request_id)

        if lead is None:  # pragma: no cover
            raise errors.LeadNotFound
        return lead


class CreateLead(UseCase):
    def __init__(self, leads: LeadRepository, llm: LLMProcessor):
        super().__init__()
        self.leads = leads
        self.llm = llm

    async def execute(self, cmd: commands.CreateLeads):
        lead = model.Lead(
            email=cmd.email,
            name=cmd.name,
            city=cmd.city,
            birthday=cmd.birthday,
            favourite_food=cmd.favourite_food,
            likes=cmd.likes,
            activities=cmd.activities,
            skin_tone=cmd.skin_tone,
            hair_color=cmd.hair_color,
            hair_length=cmd.hair_length,
            kids_photo=cmd.kids_photo,
        )
        self.leads.add(lead)
        title_prompt = ""
        # cover_prompt = ''

        title_response = await self.llm.ask_for_text(prompt=title_prompt)

        return title_response
