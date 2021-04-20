import { Filter } from '../../types/types';

export interface SearchFiltersProps {
  counties: string[];
  citiesByCounty: Record<string, Record<'cities', string[]>>;
  filters: Filter;
  onFilterChange: (
    event: React.ChangeEvent<{
      name?: string;
      value: unknown;
    }>,
    child: React.ReactNode,
  ) => void;
  onFilterReset: (event: React.FormEvent<Element>) => void;
  onFilterSubmit: (event: React.FormEvent<Element>) => void;
  saleDates: string[];
}
