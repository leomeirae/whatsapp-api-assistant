-- Criar função RPC para executar SQL diretamente
CREATE OR REPLACE FUNCTION execute_sql(query text, params text[] DEFAULT NULL)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result jsonb;
BEGIN
    IF params IS NULL THEN
        EXECUTE query INTO result;
    ELSE
        EXECUTE query USING params INTO result;
    END IF;
    
    RETURN result;
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object(
        'error', SQLERRM,
        'detail', SQLSTATE
    );
END;
$$;
