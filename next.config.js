/** @type {import('next').NextConfig} */
const path = require('path')

const nextConfig = {
  output: 'export',
  distDir: 'out',
  basePath: '/qianduo-blog',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
