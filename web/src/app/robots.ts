import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/'],
      },
      {
        userAgent: [
          'GPTBot',
          'ClaudeBot',
          'PerplexityBot',
          'Google-Extended',
          'Amazonbot',
          'Applebot-Extended',
          'Bytespider',
          'CCBot',
          'FacebookExternalHit',
        ],
        allow: '/',
        disallow: ['/api/'],
      },
    ],
    sitemap: 'https://pingdiff.com/sitemap.xml',
  };
}
