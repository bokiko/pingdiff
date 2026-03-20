import { z } from 'zod';

export const PingResultSchema = z.object({
  server_id: z.string().min(1).max(100),
  server_location: z.string().min(1).max(100),
  ping_avg: z.number().min(0).max(10000),
  ping_min: z.number().min(0).max(10000),
  ping_max: z.number().min(0).max(10000),
  jitter: z.number().min(0).max(1000),
  packet_loss: z.number().min(0).max(100),
  raw_times: z.array(z.number().min(0).max(10000)).max(100),
});

export const SubmitRequestSchema = z.object({
  game: z.string().min(1).max(50).default('overwatch-2'),
  results: z.array(PingResultSchema).min(1).max(50),
  isp: z.string().max(200).default('Unknown'),
  country: z.string().max(100).default('Unknown'),
  city: z.string().max(100).default('Unknown'),
  ip_hash: z.string().max(64).default(''),
  client_version: z.string().max(20).default('unknown'),
  anonymous_id: z.string().max(100).default('anonymous'),
});

export type PingResult = z.infer<typeof PingResultSchema>;
export type SubmitRequest = z.infer<typeof SubmitRequestSchema>;
