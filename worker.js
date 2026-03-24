export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const origin = request.headers.get('Origin') || '';
    if (!origin.startsWith('https://civicengagement.ca')) {
      return new Response('Forbidden', { status: 403 });
    }

    try {
      const url = new URL(request.url);
      const path = url.pathname;

      // Route: /geoapify/* → api.geoapify.com
      if (path.startsWith('/geoapify/')) {
        const upstream = new URL('https://api.geoapify.com' +
          path.replace('/geoapify', ''));
        url.searchParams.forEach((v, k) => upstream.searchParams.set(k, v));
        upstream.searchParams.set('apiKey', env.GEOAPIFY_KEY);

        const resp = await fetch(upstream.toString(), {
          headers: { 'User-Agent': 'CivicEngagement/1.0' }
        });
        return new Response(resp.body, {
          status: resp.status,
          headers: { ...corsHeaders, 'Content-Type': resp.headers.get('Content-Type') || 'application/json' }
        });
      }

      // Route: /proxy?url=<encoded> → CORS proxy for represent + openparliament
      if (path === '/proxy') {
        const target = url.searchParams.get('url');
        if (!target) return new Response('Missing url param', { status: 400, headers: corsHeaders });

        const targetUrl = new URL(decodeURIComponent(target));
        const allowed = ['represent.opennorth.ca', 'api.openparliament.ca'];
        if (!allowed.includes(targetUrl.hostname)) {
          return new Response('Forbidden', { status: 403, headers: corsHeaders });
        }

        const resp = await fetch(targetUrl.toString(), {
          headers: { 'Accept': 'application/json', 'User-Agent': 'CivicEngagement/1.0' }
        });
        return new Response(resp.body, {
          status: resp.status,
          headers: { ...corsHeaders, 'Content-Type': resp.headers.get('Content-Type') || 'application/json' }
        });
      }

      // Route: /civil → Pollinations AI proxy for Civil chat
      if (path === '/civil') {
        const body = await request.json();
        const resp = await fetch('https://gen.pollinations.ai/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + env.POLLINATIONS_KEY,
          },
          body: JSON.stringify(body),
        });
        return new Response(resp.body, {
          status: resp.status,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      return new Response('Not found', { status: 404, headers: corsHeaders });

    } catch (e) {
      return new Response('Worker error: ' + e.message, { status: 500, headers: corsHeaders });
    }
  }
};
