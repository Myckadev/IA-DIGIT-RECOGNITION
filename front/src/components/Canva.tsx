import React, { useRef, useState, MouseEvent, useEffect } from 'react';

export default function Canva() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [predictedNumber, setPredictedNumber] = useState<number | null>(null);
  const [accuracy, setAccuracy] = useState<number | null>(null);
  const [imageId, setImageId] = useState<string | null>(null);
  const [isDrawing, setIsDrawing] = useState<boolean>(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.lineWidth = 10;
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'white';
      }
    }
  }, []);

  const startDrawing = (e: MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.beginPath();
        ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
      }
      setIsDrawing(true);
    }
  };

  const draw = (e: MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
        ctx.stroke();
      }
    }
  };

  const endDrawing = () => {
    setIsDrawing(false);
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.closePath();
      }
    }
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }
    }
    setPredictedNumber(null);
    setAccuracy(null);
    setImageId(null);
  };

  const sendImage = async () => {
    const canvas = canvasRef.current;
    if (canvas) {
      const dataURL = canvas.toDataURL('image/png');
      try {
        const response = await fetch('http://localhost:8000/api/recognize/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: dataURL }),
        });

        const result = await response.json();
        if (response.ok) {
          setPredictedNumber(result.number);
          setAccuracy(result.accuracy);
          setImageId(result.id);
        } else {
          alert('Error: ' + result.error);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error);
      }
    }
  };

  const verifyPrediction = async (correct: boolean) => {
    if (imageId !== null && predictedNumber !== null) {
      try {
        const response = await fetch('http://localhost:8000/api/verify/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image_id: imageId,
            correct_label: correct ? predictedNumber : prompt('Enter the correct number:', '')
          }),
        });

        const result = await response.json();
        if (response.ok) {
          alert('Verification successful');
        } else {
          alert('Error: ' + result.error);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error);
      }
    }
  };

  return (
    <div>
      <h1>Dessinez un chiffre</h1>
      <canvas
        ref={canvasRef}
        width="280"
        height="280"
        style={{ border: '1px solid black' }}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={endDrawing}
        onMouseLeave={endDrawing}
      />
      <br />
      <button onClick={clearCanvas}>Effacer</button>
      <button onClick={sendImage}>Envoyer</button>
      {predictedNumber !== null && (
        <div>
          <h2>Reconnu : {predictedNumber} avec une précision de {accuracy?.toFixed(2)}%</h2>
          <button onClick={() => verifyPrediction(true)}>Vrai</button>
          <button onClick={() => verifyPrediction(false)}>Faux</button>
        </div>
      )}
    </div>
  );
}
