INSERT INTO invoice_items (
                         table_index,
                         table_description,
                         unit,
                         rate,
                         total,
                         invoice_id
                         )
                   SELECT table_index,
                          table_description,
                          unit,
                          rate,
                          total,
                          ? AS new_id
                   FROM quote_items
                   WHERE quote_id = ?;