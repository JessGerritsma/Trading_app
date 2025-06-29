export type TradeSignal = {
  symbol: string;
  action: 'buy' | 'sell' | 'hold';
  confidence: number;
};
