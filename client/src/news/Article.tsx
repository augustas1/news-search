import moment from "moment";
import { clsx } from "clsx";

export const Article = ({
  article: { title, description, link, pubDate, distance },
}: Props) => {
  return (
    <div className="my-8">
      <div className="flex flex-wrap items-baseline gap-x-2 relative">
        <div
          className={clsx(
            getDistanceColor(distance),
            "absolute -left-4 bg-green-500 w-2 h-2 rounded-full self-center"
          )}
        />

        <a
          href={link}
          target="_blank"
          className="font-medium text-xl text-sky-600 hover:text-sky-700"
        >
          {title}
        </a>

        <span className="text-xs text-gray-400">
          {moment(pubDate).format("MMM D, YYYY")}
        </span>
      </div>

      <div className="text-gray-600 text-sm">{description}</div>
    </div>
  );
};

const getDistanceColor = (distance: number) => {
  if (distance < 0.5) {
    return "bg-green-400";
  } else if (distance < 0.55) {
    return "bg-yellow-300";
  }

  return "bg-red-400";
};

interface Props {
  article: ArticleMetadata;
}

export interface ArticleMetadata {
  title: string;
  description: string;
  guid: string;
  link: string;
  pubDate: string;
  distance: number;
}
