import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 * Theme: Modern Tech (现代科技风)
 * Updated: 2026-03-04 by 智小香
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Kevin 的数字花园",
    pageTitleSuffix: " | AI 与知识管理",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "zh-CN",
    baseUrl: "https://kevin850115.github.io/oc-obdoc",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Sans SC",
        body: "Noto Sans SC",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#f0f4ff",
          lightgray: "#e0e7ff",
          gray: "#94a3b8",
          darkgray: "#475569",
          dark: "#1e293b",
          secondary: "#6366f1",
          tertiary: "#8b5cf6",
          highlight: "#3b82f6",
          textHighlight: "#6366f133",
        },
        darkMode: {
          light: "#0f172a",
          lightgray: "#1e293b",
          gray: "#64748b",
          darkgray: "#94a3b8",
          dark: "#f1f5f9",
          secondary: "#818cf8",
          tertiary: "#a78bfa",
          highlight: "#60a5fa",
          textHighlight: "#818cf833",
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
          light: "github-light",
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
