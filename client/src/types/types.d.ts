
export interface EnumeratedArrayOfObjects {
  [index: number]: { [key: string]: Object[] }
}

export interface useFetchInterface {
  [key: string]: Object[]
}

export interface Filter {
  county: string,
  city: string,
  saleDate: string,
}

export type ButtonEvent = React.ChangeEvent<HTMLButtonElement>
