INSERT INTO quote (
                    user_id,
                    title,
                    sender_name,
                    sender_details,
                    recipient_details,
                    project_details,
                    send_date,
                    ref,
                    valid_till,
                    footnote,
                    total_money
                   )
                   SELECT user_id,
                        'Copy of ' || title,
                        sender_name,
                        sender_details,
                        recipient_details,
                        project_details,
                        send_date,
                        ref,
                        valid_till,
                        footnote,
                        total_money
                   FROM quote
                   WHERE id = ?;