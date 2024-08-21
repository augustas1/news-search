import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { Article, ArticleMetadata } from './Article';

export const NewsSearch = () => {
    const [query, setQuery] = useState('');
    const { data } = useQuery({ queryKey: ['articles', query], queryFn: () => getArticles(query), enabled: !!query });

    return <>
        <input
            autoFocus
            className='px-4 py-2 border rounded-full w-full bg-gray-200 focus:outline-none focus:ring-1'
            onChange={({ target }) => setQuery(target.value)}
        />

        {data?.map(article => <Article article={article} />)}
    </>
}

const getArticles = async (query: string): Promise<ArticleMetadata[]> => {
    const params = new URLSearchParams({ query });
    const data = await fetch(`/api/articles?${params}`);
    return data.json()
}