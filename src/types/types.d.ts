import * as React from 'react';

export type Filter = {
  county: string;
  city: string;
  saleDate: string;
};

export type ButtonEvent = React.ChangeEvent<HTMLButtonElement>;

export interface ListingInterface {
  id?: number;
  address?: string;
  address_sanitized?: string;
  attorney?: string;
  attorney_phone?: string;
  city?: string;
  county?: string;
  court_case?: string;
  deed?: string;
  deed_address?: string;
  defendant?: string;
  description?: string;
  judgment?: number;
  latitude?: string | float;
  longitude?: string | float;
  maps_url?: string;
  parcel?: string;
  plaintiff?: string;
  priors?: string;
  sale_date?: string;
  secondary_unit?: string;
  sheriff?: string;
  state?: string;
  status_history?: Record<string, unknown>;
  street?: string;
  unit?: string;
  unit_secondary?: string;
  upset_amount?: number;
  zip_code?: string;
}

export interface SearchFiltersInterface {
  cities: string[];
  counties: string[];
  filters: Record<string, null>;
  filterErrors: Record<string, null>;
  njData: Record<string, null>;
  onFilterChange: React.FormEvent<Element>;
  onFilterReset: React.FormEvent<Element>;
  onFilterSubmit: React.FormEvent<Element>;
  saleDates: string[];
}
