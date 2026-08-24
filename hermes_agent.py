"""
===============================================================================
HERMES AI AGENTIC DOCUMENT PARSER & INTELLIGENT TABLE ROUTER (ENHANCED V2)
===============================================================================
"""

import os
import re
import json
import pandas as pd

class HermesAgent:
    """
    Hermes AI Agentic Parser:
    Scans unstructured documents (Excel, CSV, PDF, Text, Messy Tables),
    extracts tabular data, normalizes column headers, filters out row index/serial numbers,
    and returns a clean standardized pandas DataFrame ready for 4-point triangulation.
    """
    
    @staticmethod
    def parse_document(file_path):
        print(f"[Hermes AI Agent] 🧠 Scanning document: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        df = None

        if ext == '.csv':
            try:
                df = pd.read_csv(file_path)
            except Exception:
                df = pd.read_csv(file_path, sep=None, engine='python')
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format for Hermes AI: {ext}")

        if df is None or len(df) == 0:
            raise ValueError("Document contains no readable table data.")

        print(f"[Hermes AI Agent] Raw table extracted: {len(df)} rows, {len(df.columns)} columns.")

        df = HermesAgent._normalize_headers(df)
        company_col = HermesAgent._identify_company_column(df)
        print(f"[Hermes AI Agent] Identified primary company entity column: '{company_col}'")

        df = HermesAgent._clean_entity_column(df, company_col)
        print(f"[Hermes AI Agent] ✅ Document parsed & routed successfully.")
        return df, company_col

    @staticmethod
    def _normalize_headers(df):
        cleaned_cols = []
        for i, c in enumerate(df.columns):
            c_str = str(c).strip()
            if 'unnamed' in c_str.lower() or not c_str:
                cleaned_cols.append(f"Column_{i+1}")
            else:
                cleaned_cols.append(c_str)
        df.columns = cleaned_cols
        return df

    @staticmethod
    def _identify_company_column(df):
        keywords = ['porfolio_company', 'portfolio_company', 'portfolio company', 'company', 'borrower', 'entity', 'target', 'issuer', 'company_name']
        
        # 1. Exact or fuzzy keyword match
        for kw in keywords:
            for c in df.columns:
                if kw in str(c).lower():
                    return c

        # 2. Score text columns by proper noun / corporate entity patterns (LLC, Inc, Corp, Hldg, Ltd, LP)
        corp_pattern = re.compile(r'(?i)\b(llc|inc|corp|ltd|lp|hldg|holdings|group|co|hldgs|services|systems|partner)\b')
        best_col = None
        best_score = -1

        for c in df.columns:
            sample = df[c].dropna().astype(str)
            if len(sample) > 0:
                # Check for numeric serial column
                non_numeric = [v for v in sample[:30] if not v.replace('.', '', 1).replace('-', '', 1).isdigit()]
                if len(non_numeric) > len(sample[:30]) * 0.5:
                    # Count how many rows match company entity patterns
                    score = sum(1 for v in sample[:30] if corp_pattern.search(v))
                    if score > best_score:
                        best_score = score
                        best_col = c

        if best_col is not None:
            return best_col

        return df.columns[0]

    @staticmethod
    def _clean_entity_column(df, col):
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['nan', 'NaN', 'None', 'null', 'NULL', ''], None)
        return df

if __name__ == '__main__':
    print("Testing Enhanced Hermes AI Agentic Parser...")
    test_df, comp_col = HermesAgent.parse_document('/Users/ekramqureshi/miland data /Data abc.xlsx')
    print("Extracted Company Column:", comp_col)
    print(test_df[[comp_col]].head(10))
