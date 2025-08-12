export default async function handler(req, res) {
  const { path } = req.query;
  const apiPath = Array.isArray(path) ? path.join('/') : path;
  
  const backendUrl = `https://3.27.123.53.sslip.io/api/${apiPath}`;
  
  try {
    const response = await fetch(backendUrl, {
      method: req.method,
      headers: {
        ...req.headers,
        host: '3.27.123.53.sslip.io',
      },
      body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined,
    });

    const data = await response.text();
    
    // Forward all headers from backend response
    Object.entries(response.headers.entries()).forEach(([key, value]) => {
      res.setHeader(key, value);
    });
    
    res.status(response.status);
    
    // Try to parse as JSON, fallback to text
    try {
      res.json(JSON.parse(data));
    } catch {
      res.send(data);
    }
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ error: 'Proxy error' });
  }
}