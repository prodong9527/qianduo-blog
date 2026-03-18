/** @type {import('next').NextConfig} */
const path = require('path')

const nextConfig = {
  output: 'export',
  distDir: 'docs',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
