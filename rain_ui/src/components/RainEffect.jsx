import React, { useEffect, useRef } from 'react';
import './RainEffect.css';

const RainEffect = ({ prediction }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    // Determine rain intensity from prediction data
    // Fallback to light rain if no prediction
    const amount = prediction ? parseFloat(prediction.amount) : 0;
    
    // Baseline: Visible but not overwhelming
    let dropCount = 150; 
    let lightningChance = 0;
    
    if (prediction) {
      if (amount > 30) {
        dropCount = 250; // Heavier Rain
        lightningChance = 0.001; // Reduced lightning frequency
      } else if (amount > 10) {
        dropCount = 200;  // Moderate Rain
        lightningChance = 0.0002;
      }
    }

    // Always render canvas now

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Set canvas dimensions to window size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Raindrop class
    class Drop {
      constructor() {
        this.reset();
        // Randomize initial Y so they don't all fall from the top at once
        this.y = Math.random() * canvas.height;
      }

      reset() {
        this.x = Math.random() * canvas.width;
        this.y = -20; // Start slightly above screen
        this.length = Math.random() * 12 + 6; // Noticeable drops
        this.speed = Math.random() * 5 + 7;  // Medium speed
        this.opacity = Math.random() * 0.25 + 0.1; // Visible opacity
      }

      update() {
        this.y += this.speed;
        // Slant slightly to the left
        this.x -= this.speed * 0.1;
        
        if (this.y > canvas.height) {
          this.reset();
        }
      }

      draw() {
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x - this.length * 0.1, this.y + this.length);
        ctx.strokeStyle = `rgba(186, 230, 253, ${this.opacity})`; // Neon light blue
        ctx.lineWidth = 1.0; // Thinner
        ctx.lineCap = 'round';
        ctx.shadowBlur = 2; // Subtle glow
        ctx.shadowColor = 'rgba(56, 189, 248, 0.4)';
        ctx.stroke();
        
        // Reset shadow for performance on next draws
        ctx.shadowBlur = 0;
      }
    }

    // Initialize drops
    const drops = [];
    for (let i = 0; i < dropCount; i++) {
        drops.push(new Drop());
    }

    let animationFrameId;
    let lightningActive = false;
    let lightningDuration = 0;

    const render = () => {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Handle lightning
        if (lightningChance > 0) {
             if (lightningActive) {
                // Draw white overlay for flash
                ctx.fillStyle = `rgba(255, 255, 255, ${0.3 * (lightningDuration / 5)})`;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                lightningDuration--;
                if (lightningDuration <= 0) {
                    lightningActive = false;
                }
             } else if (Math.random() < lightningChance) {
                 lightningActive = true;
                 lightningDuration = 5; // Flash for just 5 frames
             }
        }

        // Draw and update drops
        drops.forEach(drop => {
            drop.update();
            drop.draw();
        });

        animationFrameId = requestAnimationFrame(render);
    };

    render();

    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId);
    };
  }, [prediction]);

  return (
    <canvas 
      ref={canvasRef} 
      className="rain-canvas"
    />
  );
};

export default RainEffect;
