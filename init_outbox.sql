-- Tabla Outbox para garantizar publicación atómica de eventos
CREATE TABLE IF NOT EXISTS outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(100) NOT NULL, 
    aggregate_id VARCHAR(100) NOT NULL,   
    event_type VARCHAR(100) NOT NULL,     
    payload JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',  
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX IF NOT EXISTS idx_outbox_pending ON outbox_events(status, created_at) WHERE status = 'PENDING';

-- Tabla de Control de Idempotencia para Consumidores (At-Least-Once)
CREATE TABLE IF NOT EXISTS processed_events (
    event_id UUID PRIMARY KEY,
    consumer_name VARCHAR(100) NOT NULL,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
