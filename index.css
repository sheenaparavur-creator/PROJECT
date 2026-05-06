/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Eraser, Brain, Send, RefreshCw, Layers } from 'lucide-react';

export default function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [prediction, setPrediction] = useState<number | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [isloading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 20;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
      }
    }
  }, []);

  const startDrawing = (e: React.MouseEvent | React.TouchEvent) => {
    setIsDrawing(true);
    draw(e);
  };

  const stopDrawing = () => {
    setIsDrawing(false);
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    ctx?.beginPath();
  };

  const draw = (e: React.MouseEvent | React.TouchEvent) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    let x, y;

    if ('touches' in e) {
      x = e.touches[0].clientX - rect.left;
      y = e.touches[0].clientY - rect.top;
    } else {
      x = e.clientX - rect.left;
      y = e.clientY - rect.top;
    }

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (ctx && canvas) {
      ctx.fillStyle = 'black';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      setPrediction(null);
      setConfidence(null);
      setError(null);
    }
  };

  const handlePredict = async () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    setIsLoading(true);
    setError(null);

    try {
      // Create a temporary canvas to resize the image to 28x28
      const tmpCanvas = document.createElement('canvas');
      tmpCanvas.width = 28;
      tmpCanvas.height = 28;
      const tmpCtx = tmpCanvas.getContext('2d');
      if (!tmpCtx) throw new Error('Could not create processing context');

      tmpCtx.drawImage(canvas, 0, 0, 28, 28);
      const imageData = tmpCtx.getImageData(0, 0, 28, 28);
      const data = imageData.data;
      
      // Extract grayscale values (using just the R channel since it's B&W)
      const pixels: number[] = [];
      for (let i = 0; i < data.length; i += 4) {
        // Red channel (0-255)
        pixels.push(data[i]);
      }

      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: pixels }),
      });

      if (!response.ok) {
        throw new Error('Prediction failed');
      }

      const result = await response.json();
      setPrediction(result.prediction);
      setConfidence(result.confidence);
    } catch (err) {
      console.error(err);
      setError('Connection to backend failed. Make sure the FastAPI server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-4 font-sans">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full space-y-8"
      >
        <div className="text-center space-y-2">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-indigo-500/20 rounded-2xl border border-indigo-500/30">
              <Brain className="w-8 h-8 text-indigo-400" />
            </div>
          </div>
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            MNIST Classifier
          </h1>
          <p className="text-slate-400 text-sm">
            Draw a digit (0-9) in the box below
          </p>
        </div>

        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
          <div className="relative bg-black rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
            <canvas
              ref={canvasRef}
              width={280}
              height={280}
              onMouseDown={startDrawing}
              onMouseUp={stopDrawing}
              onMouseMove={draw}
              onMouseLeave={stopDrawing}
              onTouchStart={startDrawing}
              onTouchEnd={stopDrawing}
              onTouchMove={draw}
              className="w-full aspect-square cursor-crosshair touch-none"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={clearCanvas}
            className="flex items-center justify-center gap-2 py-3 px-4 bg-slate-900 hover:bg-slate-800 rounded-xl border border-slate-800 transition-colors text-sm font-medium"
          >
            <Eraser className="w-4 h-4" />
            Clear
          </button>
          <button
            onClick={handlePredict}
            disabled={isloading}
            className="flex items-center justify-center gap-2 py-3 px-4 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 rounded-xl transition-all text-sm font-medium shadow-lg shadow-indigo-500/20"
          >
            {isloading ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            {isloading ? 'Analyzing...' : 'Predict'}
          </button>
        </div>

        <AnimatePresence>
          {(prediction !== null || error) && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className={`p-6 rounded-2xl border ${
                error ? 'bg-red-500/10 border-red-500/20' : 'bg-indigo-500/10 border-indigo-500/20'
              }`}
            >
              {error ? (
                <p className="text-red-400 text-sm text-center font-medium">{error}</p>
              ) : (
                <div className="flex items-center justify-around">
                  <div className="text-center">
                    <p className="text-xs text-indigo-400 uppercase tracking-wider font-semibold mb-1">Prediction</p>
                    <p className="text-5xl font-black text-white">{prediction}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-indigo-400 uppercase tracking-wider font-semibold mb-1">Confidence</p>
                    <p className="text-2xl font-bold text-white">
                      {(confidence! * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="flex items-center justify-center gap-6 pt-4 border-t border-slate-900 text-slate-500">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4" />
            <span className="text-[10px] uppercase font-bold tracking-widest leading-none">scikit-learn backend</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
