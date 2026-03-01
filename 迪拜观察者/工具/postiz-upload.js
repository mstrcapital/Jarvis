#!/usr/bin/env node
/**
 * Postiz 自动上传脚本
 * 
 * 功能：
 * 1. 上传视频/图片到Postiz
 * 2. 设置文案、定时发布
 * 3. 支持多平台发布
 * 
 * 使用方法：
 * 1. 修改配置（API Key、文件路径等）
 * 2. 运行: node postiz-upload.js
 * 
 * 依赖：
 * npm install axios form-data
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');

// ============================================
// 配置区域 - 修改这里的值
// ============================================

const CONFIG = {
  // Postiz API Key (在 https://postiz.com/settings/api 获取)
  API_KEY: 'c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d',
  
  // Postiz API 地址 (正确地址)
  API_BASE_URL: 'https://api.postiz.com/public/v1',
  
  // 发布配置
  publish: {
    // 定时发布时间 (ISO格式，为空则立即发布)
    scheduled_at: '', // 例: '2026-02-16T09:00:00Z'
    
    // 发布到的平台 (channels数组的ID)
    // 在Postiz后台 Channels 页面查看
    channels: ['cmlomzyp90166qf0y1qvcpzyh'],
      // 'YOUR_CHANNEL_ID_1',
      // 'YOUR_CHANNEL_ID_2',
    ],
    
    // 文案
    caption: `测试发布 - ${new Date().toLocaleString()}`,
    
    // 话题标签
    tags: ['迪拜', '阿联酋', '旅行'],
    
    // 隐私设置
    privacy: 'public', // public, private
  },
  
  // 文件配置
  file: {
    // 视频文件路径
    video: '/root/.openclaw/workspace/阿联酋风情/素材/视频/demo.mp4',
    
    // 缩略图路径（可选）
    thumbnail: '',
  },
};

// ============================================
// 主程序
// ============================================

class PostizUploader {
  constructor(config) {
    this.config = config;
    this.apiKey = config.API_KEY;
    this.baseUrl = config.API_BASE_URL;
    
    // 创建Axios实例
    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
    });
  }
  
  /**
   * 获取已连接的频道列表
   */
  async getChannels() {
    try {
      const response = await this.client.get('/channels');
      console.log('📋 已连接的频道:');
      response.data.forEach(ch => {
        console.log(`  - ${ch.name} (${ch.provider}) [ID: ${ch.id}]`);
      });
      return response.data;
    } catch (error) {
      console.error('❌ 获取频道失败:', error.message);
      return [];
    }
  }
  
  /**
   * 获取用户信息
   */
  async getUser() {
    try {
      const response = await this.client.get('/user/me');
      console.log(`👤 用户: ${response.data.name}`);
      console.log(`📧 邮箱: ${response.data.email}`);
      return response.data;
    } catch (error) {
      console.error('❌ 获取用户信息失败:', error.message);
      return null;
    }
  }
  
  /**
   * 上传视频
   */
  async uploadVideo(options = {}) {
    const {
      videoPath,
      caption,
      thumbnailPath,
      scheduledAt,
      channelIds,
      tags,
      privacy,
    } = options;
    
    console.log('📤 开始上传视频...');
    console.log(`   文件: ${videoPath}`);
    
    // 检查文件是否存在
    if (!fs.existsSync(videoPath)) {
      console.error(`❌ 文件不存在: ${videoPath}`);
      return null;
    }
    
    try {
      // 创建FormData
      const form = new FormData();
      
      // 添加视频文件
      form.append('video', fs.createReadStream(videoPath));
      
      // 添加缩略图（如果有）
      if (thumbnailPath && fs.existsSync(thumbnailPath)) {
        form.append('thumbnail', fs.createReadStream(thumbnailPath));
      }
      
      // 添加元数据
      form.append('caption', caption || this.config.publish.caption);
      form.append('privacy', privacy || this.config.publish.privacy);
      
      if (scheduledAt) {
        form.append('scheduled_at', scheduledAt);
      }
      
      if (channelIds && channelIds.length > 0) {
        form.append('channels', JSON.stringify(channelIds));
      }
      
      if (tags && tags.length > 0) {
        form.append('tags', JSON.stringify(tags));
      }
      
      // 发送请求
      const response = await this.client.post('/posts', form, {
        headers: {
          ...form.getHeaders(),
        },
      });
      
      console.log('✅ 视频上传成功!');
      console.log(`   Post ID: ${response.data.id}`);
      console.log(`   状态: ${response.data.status}`);
      console.log(`   链接: ${response.data.url}`);
      
      return response.data;
    } catch (error) {
      console.error('❌ 上传失败:', error.message);
      if (error.response) {
        console.error('   响应:', error.response.data);
      }
      return null;
    }
  }
  
  /**
   * 批量上传
   */
  async batchUpload(items) {
    console.log(`\n🚀 开始批量上传 (${items.length}个任务)`);
    console.log('='.repeat(50));
    
    const results = [];
    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      console.log(`\n📦 任务 ${i + 1}/${items.length}`);
      console.log('-'.repeat(30));
      
      const result = await this.uploadVideo(item);
      results.push({
        item,
        result,
        success: !!result,
      });
      
      // 避免请求过快，添加延迟
      if (i < items.length - 1) {
        console.log('⏳ 等待2秒后继续...');
        await new Promise(r => setTimeout(r, 2000));
      }
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('📊 批量上传结果:');
    const successCount = results.filter(r => r.success).length;
    const failCount = results.filter(r => !r.success).length;
    console.log(`   成功: ${successCount}`);
    console.log(`   失败: ${failCount}`);
    
    return results;
  }
}

// ============================================
// 使用示例
// ============================================

async function main() {
  console.log('='.repeat(50));
  console.log('🚀 Postiz 自动上传脚本 v1.0');
  console.log('='.repeat(50));
  console.log('');
  
  // 检查配置
  if (CONFIG.API_KEY === 'YOUR_POSTIZ_API_KEY') {
    console.log('⚠️  请先配置API Key!');
    console.log('   1. 登录 https://postiz.com');
    console.log('   2. 进入 Settings > API');
    console.log('   3. 复制API Key');
    console.log('   4. 修改脚本中的 CONFIG.API_KEY');
    console.log('');
    return;
  }
  
  // 创建上传器
  const uploader = new PostizUploader(CONFIG);
  
  // 获取用户信息
  await uploader.getUser();
  
  // 获取频道列表
  const channels = await uploader.getChannels();
  
  // 设置默认频道
  const defaultChannels = channels
    .filter(ch => ['youtube', 'tiktok', 'twitter'].includes(ch.provider))
    .map(ch => ch.id);
  
  // 示例：上传单个视频
  // await uploader.uploadVideo({
  //   videoPath: CONFIG.file.video,
  //   caption: '迪拜城市风光 - 测试发布',
  //   scheduledAt: CONFIG.publish.scheduled_at || null,
  //   channelIds: defaultChannels,
  //   tags: CONFIG.publish.tags,
  //   privacy: CONFIG.publish.privacy,
  // });
  
  // 示例：批量上传
  const batchItems = [
    {
      videoPath: '/root/.openclaw/workspace/阿联酋风情/素材/视频/video1.mp4',
      caption: '迪拜城市风光第一集',
      channelIds: defaultChannels,
      tags: ['迪拜', '旅行', '城市风光'],
    },
    {
      videoPath: '/root/.openclaw/workspace/阿联酋风情/素材/视频/video2.mp4',
      caption: '迪拜奢华体验第二集',
      channelIds: defaultChannels,
      tags: ['迪拜', '奢华', '酒店'],
    },
  ];
  
  // 取消注释以执行批量上传
  // await uploader.batchUpload(batchItems);
  
  console.log('\n📝 使用说明:');
  console.log('   1. 修改脚本中的 API_KEY');
  console.log('   2. 设置视频文件路径');
  console.log('   3. 运行: node postiz-upload.js');
  console.log('');
}

// 运行主程序
main().catch(console.error);

// ============================================
// 辅助函数
// ============================================

/**
 * 从素材库批量生成上传任务
 */
function generateTasksFromLibrary(libraryPath) {
  const tasks = [];
  
  // 读取素材库
  const samples = fs.readdirSync(`${libraryPath}/样本`)
    .filter(f => f.endsWith('.md'));
  
  samples.forEach(sample => {
    // 解析样本文件，提取视频路径和文案
    // 这里需要根据实际样本格式解析
    tasks.push({
      videoPath: `${libraryPath}/素材/视频/${sample.replace('.md', '.mp4')}`,
      caption: sample.replace('.md', ''),
    });
  });
  
  return tasks;
}

/**
 * 定时发布配置示例
 */
const SCHEDULE_EXAMPLES = {
  // 每天3个时段发布
  daily3Times: {
    times: ['09:00', '12:00', '21:00'],
    timezone: 'Asia/Dubai',
  },
  
  // 工作日发布
  weekdays: {
    days: [1, 2, 3, 4, 5],
    time: '12:00',
    timezone: 'Asia/Dubai',
  },
  
  // 周末发布
  weekends: {
    days: [6, 0],
    time: '10:00',
    timezone: 'Asia/Dubai',
  },
};

module.exports = {
  PostizUploader,
  generateTasksFromLibrary,
  SCHEDULE_EXAMPLES,
};