FROM node:22-alpine AS builder
WORKDIR /repo
COPY data/ ./data/
COPY web/package*.json ./web/
WORKDIR /repo/web
RUN npm ci
COPY web/ .
ARG PUBLIC_GOOGLE_CLIENT_ID
ENV PUBLIC_GOOGLE_CLIENT_ID=${PUBLIC_GOOGLE_CLIENT_ID}
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /repo/web/package*.json ./
RUN npm ci --omit=dev
COPY --from=builder /repo/web/dist/ ./dist/
EXPOSE 4321
ENV HOST=0.0.0.0
ENV PORT=4321
ENV NODE_ENV=production
CMD ["node", "./dist/server/entry.mjs"]
