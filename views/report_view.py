def report_text(blocks, date, channel_id):
    report = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":memo: *Daily Standup Report*\n\n *Report from {date}*"
                }
            },
            {
                "type": "divider"
            }
        ],
        "channel": channel_id
    }
    for block in blocks:
        report["blocks"].append(block)

    return report


def report_blocks(dailys):
    blocks = []
    if len(dailys) == 0:
        block = {
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": ":cry: *No records found*"
            }
        }
        blocks.append(block)
    else:
        for daily in dailys:
            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":technologist: *{daily.user.username}*\n*What did you do yesterday?*\n{daily.yesterday_question}\n\n*What will you do today?*\n{daily.today_question}\n\n*Are there any blockers or impediments preventing you from doing your work?*\n{daily.blockers_question}"
                }
            }
            blocks.append(block)
    return blocks
