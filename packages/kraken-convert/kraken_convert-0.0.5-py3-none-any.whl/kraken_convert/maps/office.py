

def mail():
    record = {
        "@type": "'message'",
        "@id": "str(uuid.uuid4())",
        "isPartOf": {
            "@type": "'conversation'",
            "sameAs": "'office.com/conversation/' + str(r.conversationId)",
        },
        "sender": {
            "_base": "r.sender",
            "@type": "'person'",
            "email": "r.emailAddress.address"
        },
        "toRecipient": {
            "_base": "r.toRecipients",
            "@type": "'person'",
            "email": "r.emailAddress.address",
            "givenName": "r.emailAddress.name.split(', ')[1]",
            "familyName": "r.emailAddress.name.split(', ')[0]"
        },
        "ccRecipient": {
            "_base": "r.ccRecipients",
            "@type": "'person'",
            "email": "r.emailAddress.address",
            "givenName": "r.emailAddress.name.split(', ')[1]",
            "familyName": "r.emailAddress.name.split(', ')[0]"
        },
        "bccRecipient": {
            "_base": "r.bccRecipients",
            "@type": "'person'",
            "email": "r.emailAddress.address",
            "givenName": "r.emailAddress.name.split(', ')[1]",
            "familyName": "r.emailAddress.name.split(', ')[0]"
        },
        "dateSent": "",
        "dateReceived": "r.receivedDateTime",
        "headline": "r.subject",
        "abstract": "r.bodyPreview",
        "sameAs": "'office.com/mail/' + str(r.id)",
        "text": "r.body.content"
    }
    return record