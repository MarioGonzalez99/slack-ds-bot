ds_view = {
    "title": {
        "type": "plain_text",
        "text": "Daily Standup"
    },
    "submit": {
        "type": "plain_text",
        "text": "Submit"
    },
    "blocks": [
        {
            "type": "input",
            "element": {
                    "type": "datepicker",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True
                    },
                "action_id": "date-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Date",
                "emoji": True
            },
            "block_id": "date-block"
        },
        {
            "type": "input",
            "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "yesterday-action"
            },
            "label": {
                "type": "plain_text",
                "text": "What did you do yesterday?",
                "emoji": True
            },
            "block_id": "yesterday-block"
        },
        {
            "type": "input",
            "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "today-action"
            },
            "label": {
                "type": "plain_text",
                "text": "What will you do today?",
                "emoji": True
            },
            "block_id": "today-block"
        },
        {
            "type": "input",
            "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "blockers-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Are there any blockers or impediments preventing you from doing your work?",
                "emoji": True
            },
            "block_id": "blockers-block"
        }
    ],
    "type": "modal"
}
