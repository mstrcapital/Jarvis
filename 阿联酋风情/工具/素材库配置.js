/**
 * 素材库配置 - 多平台管理
 * 
 * 每个素材库独立配置，支持一键切换
 * 
 * 使用方法:
 * const config = require('./素材库配置');
 * const myConfig = config.阿联酋风情;
 */

const CONFIG = {
  // ============================================
  // 1. 阿联酋风情 → TikTok
  // ============================================
  阿联酋风情: {
    name: '阿联酋风情',
    platform: 'TikTok',
    path: '/root/.openclaw/workspace/阿联酋风情',
    apiKey: 'c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d',
    contentType: '短视频',
    style: '争议性、话题性、情绪化',
    publishConfig: {
      scheduled_at: '', // 立即发布
      channels: ['cmlomzyp90166qf0y1qvcpzyh'], // TikTok Channel ID
      tags: ['迪拜', '阿联酋', '旅行', '奢华'],
      privacy: 'public',
    },
    fileConfig: {
      video: '/root/.openclaw/workspace/阿联酋风情/素材/视频',
      thumbnail: '/root/.openclaw/workspace/阿联酋风情/素材/封面',
    },
  },

  // ============================================
  // 2. 迪拜影像 → Instagram
  // ============================================
  迪拜影像: {
    name: '迪拜影像',
    platform: 'Instagram',
    path: '/root/.openclaw/workspace/迪拜影像',
    apiKey: 'c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d',
    contentType: '图片/短视频',
    style: '高颜值、视觉系、精美',
    publishConfig: {
      scheduled_at: '2026-02-16T09:00:00Z', // 定时9:00
      channels: ['cmlon7x9a016jqf0y440vzy3d'], // Instagram Channel ID
      tags: ['dubai', 'photography', 'luxury', 'travel'],
      privacy: 'public',
    },
    fileConfig: {
      video: '/root/.openclaw/workspace/迪拜影像/素材/视频',
      image: '/root/.openclaw/workspace/迪拜影像/素材/图片',
      thumbnail: '/root/.openclaw/workspace/迪拜影像/素材/封面',
    },
  },

  // ============================================
  // 3. 中东快讯 → X (Twitter)
  // ============================================
  中东快讯: {
    name: '中东快讯',
    platform: 'X (Twitter)',
    path: '/root/.openclaw/workspace/中东快讯',
    apiKey: 'c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d',
    contentType: '短图文/新闻',
    style: '新闻、观点、互动',
    publishConfig: {
      scheduled_at: '2026-02-16T12:00:00Z', // 定时12:00
      channels: ['cmlomo6nn015kqf0y9re6jw09'], // X Channel ID
      tags: ['Dubai', 'MiddleEast', 'News', 'Tech'],
      privacy: 'public',
    },
    fileConfig: {
      image: '/root/.openclaw/workspace/中东快讯/素材/图片',
      thumbnail: '/root/.openclaw/workspace/中东快讯/素材/封面',
    },
  },
};

// ============================================
// 辅助函数
// ============================================

/**
 * 获取指定素材库的配置
 */
function getConfig(libraryName) {
  if (CONFIG[libraryName]) {
    return CONFIG[libraryName];
  }
  throw new Error(`素材库不存在: ${libraryName}`);
}

/**
 * 获取所有素材库列表
 */
function listLibraries() {
  return Object.keys(CONFIG).map(name => ({
    name,
    platform: CONFIG[name].platform,
    path: CONFIG[name].path,
  }));
}

/**
 * 切换素材库
 */
function switchLibrary(libraryName) {
  const config = getConfig(libraryName);
  console.log(`\n切换到: ${config.name}`);
  console.log(`平台: ${config.platform}`);
  console.log(`路径: ${config.path}`);
  return config;
}

module.exports = {
  CONFIG,
  getConfig,
  listLibraries,
  switchLibrary,
};