import type { ReactNode } from 'react'

const renderInline = (value: string): ReactNode[] => {
  const parts = value.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index} className="font-semibold text-[var(--ink)]">{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={index} className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-[0.85em] text-[var(--ink)]">{part.slice(1, -1)}</code>
    }
    return <span key={index}>{part}</span>
  })
}

export const MarkdownMessage = ({ content }: { content: string }) => {
  const normalizedContent = content
    .replace(/\\([*_`#>-])/g, '$1')
    .replace(/\u00a0/g, ' ')
  const lines = normalizedContent.split(/\r?\n/)
  const blocks: ReactNode[] = []
  let paragraph: string[] = []
  let list: string[] = []
  let orderedList: string[] = []
  let code: string[] = []
  let codeLanguage = ''
  let inCode = false

  const flushParagraph = () => {
    if (paragraph.length) {
      blocks.push(<p key={`p-${blocks.length}`}>{renderInline(paragraph.join(' '))}</p>)
      paragraph = []
    }
  }

  const flushLists = () => {
    if (list.length) {
      blocks.push(<ul key={`ul-${blocks.length}`} className="my-2 list-disc space-y-1 pl-5">{list.map((item, index) => <li key={index}>{renderInline(item)}</li>)}</ul>)
      list = []
    }
    if (orderedList.length) {
      blocks.push(<ol key={`ol-${blocks.length}`} className="my-2 list-decimal space-y-1 pl-5">{orderedList.map((item, index) => <li key={index}>{renderInline(item)}</li>)}</ol>)
      orderedList = []
    }
  }

  const flushText = () => {
    flushParagraph()
    flushLists()
  }

  lines.forEach((line, index) => {
    if (line.trim().startsWith('```')) {
      if (inCode) {
        blocks.push(<pre key={`code-${blocks.length}`} className="my-3 overflow-x-auto rounded-xl bg-[#0b1220] p-4 font-mono text-xs leading-6 text-slate-200"><code data-language={codeLanguage}>{code.join('\n')}</code></pre>)
        code = []
        codeLanguage = ''
        inCode = false
      } else {
        flushText()
        codeLanguage = line.trim().slice(3)
        inCode = true
      }
      return
    }

    if (inCode) {
      code.push(line)
      return
    }

    const heading = line.match(/^(#{1,3})\s+(.+)$/)
    if (heading) {
      flushText()
      const level = heading[1].length
      const Heading = level === 1 ? 'h3' : level === 2 ? 'h4' : 'h5'
      blocks.push(<Heading key={`heading-${index}`} className="mt-4 first:mt-0 font-bold text-[var(--ink)]">{renderInline(heading[2])}</Heading>)
      return
    }

    const bullet = line.match(/^\s*[-*]\s+(.+)$/)
    if (bullet) {
      flushParagraph()
      if (orderedList.length) flushLists()
      list.push(bullet[1])
      return
    }

    const ordered = line.match(/^\s*\d+\.\s+(.+)$/)
    if (ordered) {
      flushParagraph()
      if (list.length) flushLists()
      orderedList.push(ordered[1])
      return
    }

    if (!line.trim()) {
      flushText()
      return
    }

    if (list.length || orderedList.length) flushLists()
    paragraph.push(line.trim())
  })

  if (inCode) {
    blocks.push(<pre key={`code-${blocks.length}`} className="my-3 overflow-x-auto rounded-xl bg-[#0b1220] p-4 font-mono text-xs leading-6 text-slate-200"><code data-language={codeLanguage}>{code.join('\n')}</code></pre>)
  }
  flushText()

  return <div className="assistant-markdown">{blocks}</div>
}
