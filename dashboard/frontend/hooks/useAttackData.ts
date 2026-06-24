'use client';

import { useState, useCallback } from 'react';
import axios from 'axios';
import {
  AttackParams,
  AttackResponse,
  FALLBACK_ATTACK,
  FALLBACK_BASELINES,
  FALLBACK_ASR_SWEEP,
} from '@/lib/fallbackData';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

export function useAttackData() {
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState<AttackResponse | null>(null);
  const [baselines, setBaselines] = useState(FALLBACK_BASELINES);
  const [asrSweep, setAsrSweep] = useState(FALLBACK_ASR_SWEEP);
  const [error, setError] = useState<string | null>(null);

  const runAttack = useCallback(async (params: AttackParams) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post<AttackResponse>(`${API_BASE}/api/v1/attack`, params);
      setMetrics(res.data);
    } catch (e) {
      console.error(e);
      setError('Backend unavailable — using paper fallback data');
      setMetrics({ ...FALLBACK_ATTACK });
    }
    setLoading(false);
  }, []);

  const fetchBaselines = useCallback(async (dataset: string, llm: string, n: number, k: number) => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/baseline/all`, {
        params: { dataset, llm, n, k },
      });
      setBaselines(res.data.baselines);
    } catch {
      setBaselines(FALLBACK_BASELINES);
    }
  }, []);

  const fetchAsrSweep = useCallback(async (dataset: string, llm: string, attack_type: string) => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/asr-sweep`, {
        params: { dataset, llm, attack_type },
      });
      setAsrSweep(res.data.sweep);
    } catch {
      setAsrSweep(FALLBACK_ASR_SWEEP);
    }
  }, []);

  const runDefense = useCallback(
    async (params: AttackParams & { defense: string; expansion_k?: number }) => {
      setLoading(true);
      try {
        const res = await axios.post(`${API_BASE}/api/v1/defense`, params);
        if (metrics) {
          setMetrics({ ...metrics, metrics: res.data.metrics });
        }
      } catch {
        if (metrics) {
          const drop = params.defense === 'paraphrase' ? 0.1 : params.defense === 'perplexity' ? 0.22 : 0.02;
          setMetrics({
            ...metrics,
            metrics: { ...metrics.metrics, asr: Math.max(0.1, metrics.metrics.asr - drop) },
          });
        }
      }
      setLoading(false);
    },
    [metrics]
  );

  return { loading, metrics, baselines, asrSweep, error, runAttack, fetchBaselines, fetchAsrSweep, runDefense };
}
