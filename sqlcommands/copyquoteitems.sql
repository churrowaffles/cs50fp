INSERT INTO quote_items (
                         table_index,
                         table_description,
                         unit,
                         rate,
                         total,
                         quote_id
                         )
                   SELECT table_index,
                          table_description,
                          unit,
                          rate,
                          total,
                          ? AS new_id
                   FROM quote_items
                   WHERE quote_id = ?;