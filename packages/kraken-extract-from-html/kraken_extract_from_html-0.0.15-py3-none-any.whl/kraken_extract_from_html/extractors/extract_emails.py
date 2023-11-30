



def get(emails):
    return _extract_emails(emails)

def extract_emails(emails):
    return _extract_emails(emails)



def _extract_emails(emails):

    schemas = []
    for email in emails:
        record = {
            '@type': 'schema:contactPoint',
            'schema:email': email
            }

        schemas.append(record)

    return schemas
