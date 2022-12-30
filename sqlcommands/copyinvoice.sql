INSERT INTO invoice (
                    user_id,
                    title,
                    sender_name,
                    sender_details,
                    recipient_details,
                    project_details,
                    send_date,
                    ref,
                    due_date,
                    footnote,
                    total_money,
                    status,
                    status_date
                   )
                   SELECT user_id,
                        'Copy of ' || title,
                        sender_name,
                        sender_details,
                        recipient_details,
                        project_details,
                        send_date,
                        ref,
                        due_date,
                        footnote,
                        total_money,
                        status,
                        status_date
                   FROM invoice
                   WHERE id = ?;