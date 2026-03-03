import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 * Theme: Deep Blue Tech (深蓝科技风)
 * Updated: 2026-03-04 by 智小香
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Kevin 的数字花园",
    pageTitleSuffix: " | AI 与知识管理",
    enableSPA: false,  // 禁用 SPA 避免路由问题
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "zh-CN",
    baseUrl: "kevin850115.github.io/oc-obdoc",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Inter",
        body: "Inter",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#0f172a",      // 深蓝黑背景
          lightgray: "#1e293b",  // 深蓝灰
          gray: "#475569",       // 中灰
          darkgray: "#94a3b8",   // 浅灰
          dark: "#f1f5f9",       // 浅白文字
          secondary: "#3b82f6",  // 蓝色（主色）
          tertiary: "#10b981",   // 绿色（辅助色）
          highlight: "#60a5fa",  // 浅蓝高亮
          textHighlight: "#3b82f633", // 蓝色高亮背景
        },
        darkMode: {
          light: "#020617",      // 更深的背景
          lightgray: "#0f172a",  // 深蓝
          gray: "#334155",       // 中灰
          darkgray: "#94a3b8",   // 浅灰
          dark: "#f8fafc",       // 纯白文字
          secondary: "#60a5fa",  // 浅蓝
          tertiary: "#34d399",   // 浅绿
          highlight: "#93c5fd",  // 更浅的蓝
          textHighlight: "#60a5fa33",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-dark",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
