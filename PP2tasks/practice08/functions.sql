-- 1. Search contacts by pattern
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM contacts
    WHERE name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$;

-- 2. Pagination function
CREATE OR REPLACE FUNCTION get_contacts_page(lim INTEGER, off INTEGER)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM contacts
    ORDER BY id
    LIMIT lim
    OFFSET off;
END;
$$;