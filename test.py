from ts.services.contacts_service import gen_random_contact
import uuid

print(gen_random_contact(str(uuid.uuid4()), str(uuid.uuid4())).__dict__)
