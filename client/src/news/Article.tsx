export const Article = ({ article: { title, description, link } }: Props) => {
    return <div className="my-8">
        <a href={link} target="_blank" className="font-medium text-xl text-sky-600 hover:text-sky-700">{title}</a>
        <div className="text-gray-600">{description}</div>
    </div>
}

interface Props {
    article: ArticleMetadata
}

export interface ArticleMetadata {
    title: string;
    description: string;
    guid: string;
    link: string;
    pubDate: string;
    distance: number;
}