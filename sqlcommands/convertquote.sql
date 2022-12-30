INSERT INTO invoice (
                    user_id,
                    title,
                    sender_name,
                    sender_details,
                    recipient_details,
                    project_details,
                    ref,
                    footnote,
                    total_money
                   )
                   SELECT user_id,
                        'Converted from "' || title || '"',
                        sender_name,
                        sender_details,
                        recipient_details,
                        project_details,
                        ref,
                        footnote,
                        total_money
                   FROM quote
                   WHERE id = ?;