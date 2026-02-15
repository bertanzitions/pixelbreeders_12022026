import { useRef, useCallback } from 'react';

/**
 * A custom hook using IntersectionObserver.
 * it returns a lastElementRef callback that is attached to the last rendered element.
 * It automatically triggers the onLoadMore function to fetch new data.
 * isLoading - Prevents triggering a new fetch if one is already in progress.
 * hasMore - Checks if there is actually more data to load before triggering.
 * onLoadMore - The function to execute to load the next page of results.
 * A callback ref to assign to the last DOM node in the list.
 */
export const useInfiniteScroll = (
  isLoading: boolean, 
  hasMore: boolean, 
  onLoadMore: () => void
) => {
  const observer = useRef<IntersectionObserver | null>(null);

  const lastElementRef = useCallback((node: HTMLDivElement | null) => {
    if (isLoading) return;
    if (observer.current) observer.current.disconnect();

    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        onLoadMore();
      }
    });

    if (node) observer.current.observe(node);
  }, [isLoading, hasMore, onLoadMore]);

  return lastElementRef;
};