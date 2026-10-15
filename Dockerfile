# ===== Build Stage =====
FROM node:20-alpine AS builder

WORKDIR /app

COPY . .

# ===== Runtime Stage =====
FROM node:20-alpine

WORKDIR /app

# Crear usuario no-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app /app

USER appuser

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["sh", "-c", "echo Backend MediTriage iniciado && sleep infinity"]
