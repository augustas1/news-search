import { useInfiniteQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Article, ArticleMetadata } from "./Article";
import { useDebounce } from "use-debounce";
import { clsx } from "clsx";
import { useInView } from "react-intersection-observer";

export const NewsSearch = () => {
  const [query, setQuery] = useState("");
  const [debouncedQuery] = useDebounce(query, 300);

  const { data, isPending, isFetchingNextPage, fetchNextPage } =
    useInfiniteQuery({
      queryKey: ["articles", debouncedQuery],
      queryFn: ({ pageParam }) => getArticles(debouncedQuery, pageParam),
      enabled: !!debouncedQuery,
      initialPageParam: 0,
      getNextPageParam: (lastPage, _, lastPageParam) =>
        lastPage.length > 0 ? lastPageParam + 1 : undefined,
    });

  const { ref: paginatorRef } = useInView({
    onChange: (inView) => {
      if (inView) {
        fetchNextPage();
      }
    },
  });

  const loading = query && (query !== debouncedQuery || isPending);
  const allData = data?.pages.flatMap((dataPage) => dataPage);

  return (
    <>
      <input
        autoFocus
        placeholder="Search for news"
        className="px-4 py-2 border rounded-full w-full bg-gray-200 focus:outline-none focus:ring-1"
        onChange={({ target }) => setQuery(target.value)}
      />

      {loading
        ? renderPlaceholder()
        : query && (
            <>
              {allData?.map((article, index) => (
                <Article article={article} key={index} />
              ))}

              {allData?.length === 0 && (
                <div className="my-8 text-gray-400 text-sm">
                  No relevant news articles have been found.
                </div>
              )}

              {isFetchingNextPage ? (
                renderPlaceholder()
              ) : (
                <div ref={paginatorRef} />
              )}
            </>
          )}
    </>
  );
};

const renderPlaceholder = () =>
  Array(20)
    .fill(undefined)
    .map((_, index) => (
      <div className="my-8 space-y-2" key={index}>
        <div className={clsx("h-6 w-2/3", placeholderClass)} />
        <div className={clsx("h-4 w-3/4", placeholderClass)} />
      </div>
    ));

const getArticles = async (
  query: string,
  page: number
): Promise<ArticleMetadata[]> => {
  const params = new URLSearchParams({
    query,
    limit: pageSize.toString(),
    offset: (page * pageSize).toString(),
  });

  const data = await fetch(`/api/articles?${params}`);
  return data.json();
};

const pageSize = 15;
const placeholderClass =
  "bg-gradient-to-r from-gray-100 to-gray-300 animate-pulse";
