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
        "likes": lead.likes,
        "activities": lead.activities,
        "skin_tone": lead.skin_tone,
        "hair_color": lead.hair_color,
        "hair_length": lead.hair_length,
        "kids_photo": lead.kids_photo,
    }


def _db_to_model(lead):
    return Lead(
        id=lead["id"],
        email=lead["email"],
        name=lead["name"],
        city=lead["city"],
        birthday=lead["birthday"],
        favourite_food=lead["favourite_food"],
        likes=lead["likes"],
        activities=lead["activities"],
        skin_tone=lead["skin_tone"],
        hair_color=lead["hair_color"],
        hair_length=lead["hair_length"],
        kids_photo=lead["kids_photo"],
    )


class LeadSqlRepository(LeadRepository, SqlRepository):
    def add(self, lead: Lead) -> Lead:
        return self.db["leads"].insert_one(_model_to_db(lead))

    def get(self, lead_id: str) -> Lead:
        return _db_to_model(self.db["leads"].find_one({"id": lead_id}))

    def list(self) -> list[Lead]:
        leads = self.db["leads"].find({})
        return [_db_to_model(msg) for msg in leads]
