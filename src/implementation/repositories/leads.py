from domain.leads import model
from domain.leads.model import Lead
from domain.leads.repositories import LeadRepository
from implementation.sql import SqlRepository


def _model_to_db(lead: model.Lead):
    return {
        "id": lead.id,
        "email": lead.email,
        "name": lead.name,
        "city": lead.city,
        "birthday": lead.birthday,
        "favourite_food": lead.favourite_food,
        "interests": lead.interests,
        "event_to_come": lead.event_to_come,
        "skin_tone": lead.skin_tone,
        "hair_color": lead.hair_color,
        "hair_length": lead.hair_length,
        "kids_photo": lead.kids_photo,
        "result_title": lead.result.title,
        "story_message": lead.story_message,
        "favourite_place": lead.favourite_place,
        "personal_dedication": lead.personal_dedication,
        "status": lead.status,
        "result_character_url": lead.result.cover_url,
        "character_url": lead.result.character_url,
        "final_result_url": lead.result.final_result_url,
    }


def _db_to_model(lead):
    return Lead(
        id=lead["id"],
        email=lead["email"],
        name=lead["name"],
        city=lead["city"],
        birthday=lead["birthday"],
        favourite_food=lead["favourite_food"],
        interests=lead["interests"],
        event_to_come=lead["event_to_come"],
        skin_tone=lead["skin_tone"],
        hair_color=lead["hair_color"],
        hair_length=lead["hair_length"],
        kids_photo=lead["kids_photo"],
        status=lead["status"],
        favourite_place=lead["favourite_place"],
        story_message=lead["story_message"],
        personal_dedication=lead["personal_dedication"],
        result=model.Result(
            title=lead["result_title"],
            cover_url=lead["result_character_url"],
            character_url=lead["character_url"],
            final_result_url=lead["final_result_url"],
        ),
    )


class LeadSqlRepository(LeadRepository, SqlRepository):
    def add(self, lead: Lead):
        return self.db["leads"].insert_one(_model_to_db(lead))

    def get(self, lead_id: str) -> Lead:
        return _db_to_model(self.db["leads"].find_one({"id": lead_id}))

    def list(self) -> list[Lead]:
        leads = self.db["leads"].find({})
        return [_db_to_model(msg) for msg in leads]
