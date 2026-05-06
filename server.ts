import express from "express";
import { createServer as createViteServer } from "vite";
import { spawn, execSync } from "child_process";
import path from "path";
import fs from "fs";

async function startServer() {
  const app = express();
  const PORT = 3000;
  const PYTHON_PORT = 3001;

  // Check if we need to install Python dependencies
  // Note: This is a best-effort approach in this environment.
  try {
    console.log("Checking Python environment...");
    // We try to run a simple check
    execSync("python3 --version");
    console.log("Python 3 found.");
    
    // Install requirements if possible (might take time)
    console.log("Ensuring Python dependencies are installed...");
    // Running this as a separate process to not block Express too long 
    // but uvicorn will fail if they aren't there.
    // In a real environment, you'd do this once.
    const pipProcess = spawn("pip3", ["install", "-r", "requirements.txt"]);
    pipProcess.stdout.on("data", (data) => console.log(`[Pip]: ${data}`));
    pipProcess.stderr.on("data", (data) => console.error(`[Pip Error]: ${data}`));
    
    pipProcess.on("close", (code) => {
      if (code === 0) {
        console.log("Python dependencies installed successfully.");
        startPythonBackend();
      } else {
        console.error("Failed to install Python dependencies. Backend might not start.");
        // Try starting anyway in case they are already there
        startPythonBackend();
      }
    });

  } catch (err) {
    console.error("Python 3 not found in the environment. Please ensure Python is installed.");
  }

  function startPythonBackend() {
    console.log("Starting Python FastAPI backend on port " + PYTHON_PORT);
    const pythonProcess = spawn("python3", ["-m", "uvicorn", "app:app", "--port", PYTHON_PORT.toString(), "--host", "127.0.0.1"]);

    pythonProcess.stdout.on("data", (data) => {
      console.log(`[FastAPI]: ${data}`);
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`[FastAPI Error]: ${data}`);
    });

    pythonProcess.on("close", (code) => {
      console.log(`FastAPI process exited with code ${code}`);
    });
    
    // Ensure python process dies when node dies
    process.on('exit', () => pythonProcess.kill());
  }

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    if (fs.existsSync(distPath)) {
      app.use(express.static(distPath));
      app.get('*', (req, res) => {
        res.sendFile(path.join(distPath, 'index.html'));
      });
    } else {
      console.warn("Dist folder not found. Make sure to run 'npm run build'.");
    }
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Vite/Express Server running on http://localhost:${PORT}`);
  });
}

startServer();
