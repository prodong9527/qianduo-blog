/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  basePath: '/qianduo-blog',
  images: {
    unoptimized: true,
  },
  // 静态导出时需要配置
  trailingSlash: true,
}

module.exports = nextConfig
